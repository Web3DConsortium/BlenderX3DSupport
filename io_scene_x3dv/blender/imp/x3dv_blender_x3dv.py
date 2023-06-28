# SPDX-License-Identifier: Apache-2.0
# Copyright 2018-2021 The x3dv-Blender-IO authors.

import bpy
from mathutils import Vector, Quaternion, Matrix


class BlenderX3DV():
    """Main x3dv import class."""
    def __new__(cls, *args, **kwargs):
        raise RuntimeError("%s should not be instantiated" % cls)

    @staticmethod
    def create(x3dv):
        """Create x3dv main method"""

        BlenderX3DV._create(x3dv)

    @staticmethod
    def _create(x3dv):
        """Create x3dv main worker method."""
        BlenderX3DV.set_convert_functions(x3dv)
        BlenderX3DV.pre_compute(x3dv)
        BlenderScene.create(x3dv)

    @staticmethod
    def set_convert_functions(x3dv):
        if bpy.app.debug_value != 100:
            # Unit conversion factor in (Blender units) per meter
            u = 1.0 / bpy.context.scene.unit_settings.scale_length

            # x3dv Y-Up space --> Blender Z-up space
            # X,Y,Z --> X,-Z,Y
            def convert_loc(x): return u * Vector([x[0], -x[2], x[1]])
            def convert_quat(q): return Quaternion([q[3], q[0], -q[2], q[1]])
            def convert_scale(s): return Vector([s[0], s[2], s[1]])
            def convert_matrix(m):
                return Matrix([
                    [   m[0],   -m[ 8],    m[4],  m[12]*u],
                    [  -m[2],    m[10],   -m[6], -m[14]*u],
                    [   m[1],   -m[ 9],    m[5],  m[13]*u],
                    [ m[3]/u, -m[11]/u,  m[7]/u,    m[15]],
                ])

            # Batch versions operate in place on a numpy array
            def convert_locs_batch(locs):
                # x,y,z -> x,-z,y
                locs[:, [1,2]] = locs[:, [2,1]]
                locs[:, 1] *= -1
                # Unit conversion
                if u != 1: locs *= u
            def convert_normals_batch(ns):
                ns[:, [1,2]] = ns[:, [2,1]]
                ns[:, 1] *= -1

            # Correction for cameras and lights.
            # x3dv: right = +X, forward = -Z, up = +Y
            # x3dv after Yup2Zup: right = +X, forward = +Y, up = +Z
            # Blender: right = +X, forward = -Z, up = +Y
            # Need to carry Blender --> x3dv after Yup2Zup
            x3dv.camera_correction = Quaternion((2**0.5/2, 2**0.5/2, 0.0, 0.0))

        else:
            def convert_loc(x): return Vector(x)
            def convert_quat(q): return Quaternion([q[3], q[0], q[1], q[2]])
            def convert_scale(s): return Vector(s)
            def convert_matrix(m):
                return Matrix([m[0::4], m[1::4], m[2::4], m[3::4]])

            def convert_locs_batch(_locs): return
            def convert_normals_batch(_ns): return

            # Same convention, no correction needed.
            x3dv.camera_correction = None

        x3dv.loc_x3dv_to_blender = convert_loc
        x3dv.locs_batch_x3dv_to_blender = convert_locs_batch
        x3dv.quaternion_x3dv_to_blender = convert_quat
        x3dv.normals_batch_x3dv_to_blender = convert_normals_batch
        x3dv.scale_x3dv_to_blender = convert_scale
        x3dv.matrix_x3dv_to_blender = convert_matrix

    @staticmethod
    def pre_compute(x3dv):
        """Pre compute, just before creation."""
        # default scene used
        x3dv.blender_scene = None

        # Check if there is animation on object
        # Init is to False, and will be set to True during creation
        x3dv.animation_object = False

        # Blender material
        if x3dv.data.materials:
            for material in x3dv.data.materials:
                material.blender_material = {}

        # images
        if x3dv.data.images is not None:
            for img in x3dv.data.images:
                img.blender_image_name = None

        if x3dv.data.nodes is None:
            # Something is wrong in file, there is no nodes
            return

        for node in x3dv.data.nodes:
            # Weight animation management
            node.weight_animation = False

        # Dispatch animation
        if x3dv.data.animations:
            for node in x3dv.data.nodes:
                node.animations = {}

            track_names = set()
            for anim_idx, anim in enumerate(x3dv.data.animations):
                # Pick pair-wise unique name for each animation to use as a name
                # for its NLA tracks.
                desired_name = anim.name or "Anim_%d" % anim_idx
                anim.track_name = Blenderx3dv.find_unused_name(track_names, desired_name)
                track_names.add(anim.track_name)

                for channel_idx, channel in enumerate(anim.channels):
                    if channel.target.node is None:
                        continue

                    if anim_idx not in x3dv.data.nodes[channel.target.node].animations.keys():
                        x3dv.data.nodes[channel.target.node].animations[anim_idx] = []
                    x3dv.data.nodes[channel.target.node].animations[anim_idx].append(channel_idx)
                    # Manage node with animation on weights, that are animated in meshes in Blender (ShapeKeys)
                    if channel.target.path == "weights":
                        x3dv.data.nodes[channel.target.node].weight_animation = True

        # Meshes
        if x3dv.data.meshes:
            for mesh in x3dv.data.meshes:
                mesh.blender_name = {}  # caches Blender mesh name

        # Calculate names for each mesh's shapekeys
        for mesh in x3dv.data.meshes or []:
            mesh.shapekey_names = []
            used_names = set(['Basis']) #Be sure to not use 'Basis' name at import, this is a reserved name

            # Look for primitive with morph targets
            for prim in (mesh.primitives or []):
                if not prim.targets:
                    continue

                for sk, _ in enumerate(prim.targets):
                    # Skip shape key for target that doesn't morph POSITION
                    morphs_position = any(
                        (prim.targets and 'POSITION' in prim.targets[sk])
                        for prim in mesh.primitives
                    )
                    if not morphs_position:
                        mesh.shapekey_names.append(None)
                        continue

                    shapekey_name = None

                    # Try to use name from extras.targetNames
                    try:
                        shapekey_name = str(mesh.extras['targetNames'][sk])
                    except Exception:
                        pass

                    # Try to get name from first primitive's POSITION accessor
                    if shapekey_name is None:
                        try:
                            shapekey_name = x3dv.data.accessors[mesh.primitives[0].targets[sk]['POSITION']].name
                        except Exception:
                            pass

                    if shapekey_name is None:
                        shapekey_name = "target_" + str(sk)

                    shapekey_name = Blenderx3dv.find_unused_name(used_names, shapekey_name)
                    used_names.add(shapekey_name)

                    mesh.shapekey_names.append(shapekey_name)

                break



    @staticmethod
    def find_unused_name(haystack, desired_name):
        """Finds a name not in haystack and <= 63 UTF-8 bytes.
        (the limit on the size of a Blender name.)
        If a is taken, tries a.001, then a.002, etc.
        """
        stem = desired_name[:63]
        suffix = ''
        cntr = 1
        while True:
            name = stem + suffix

            if len(name.encode('utf-8')) > 63:
                stem = stem[:-1]
                continue

            if name not in haystack:
                return name

            suffix = '.%03d' % cntr
            cntr += 1


