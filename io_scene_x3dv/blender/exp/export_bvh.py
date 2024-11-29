# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

# Script copyright (C) Campbell Barton
# fixes from Andrea Rugliancich

import bpy
import sys
import os
import random

from x3d import *
from .RoundArray import round_array, round_array_no_unit_scale

def write_animation(obj):  # pass armature object

    values = []
    root_found = False

    def ensure_rot_order(rot_order_str):
        if set(rot_order_str) != {'X', 'Y', 'Z'}:
            rot_order_str = "XZY"
        return rot_order_str

    from mathutils import Matrix, Euler
    from math import degrees

    arm = obj.data
    node = None
    rotate_mode = 'XZY'
    root_transform_only=False

    # Build a dictionary of children.
    # None for parentless
    children = {None: []}

    # initialize with blank lists
    for bone in arm.bones:
        children[bone.name] = []

    # keep bone order from armature, no sorting, not esspential but means
    # we can maintain order from import -> export which secondlife incorrectly expects.
    for bone in arm.bones:
        children[getattr(bone.parent, "name", None)].append(bone.name)

    # bone name list in the order that the bones are written
    serialized_names = []

    node_locations = {}

    def write_recursive_nodes(bone_name):
        my_children = children[bone_name]

        bone = arm.bones[bone_name]
        pose_bone = obj.pose.bones[bone_name]
        loc = bone.head_local
        node_locations[bone_name] = loc

        if rotate_mode == "NATIVE":
            rot_order_str = ensure_rot_order(pose_bone.rotation_mode)
        else:
            rot_order_str = rotate_mode

        # make relative if we can
        if bone.parent:
            loc = loc - node_locations[bone.parent.name]

        if my_children:
            # store the location for the children
            # to get their relative offset

            # Write children
            for child_bone in my_children:
                serialized_names.append(child_bone)
                write_recursive_nodes(child_bone)

        else:
            # Write the bone end.
            loc = bone.tail_local - node_locations[bone_name]
            values.append(round_array(loc)[:]) # location
            root_found = True

    if len(children[None]) == 1:
        key = children[None][0]
        serialized_names.append(key)

        write_recursive_nodes(key)

    else:
        for child_bone in children[None]:
            serialized_names.append(child_bone)
            write_recursive_nodes(child_bone)

    class DecoratedBone:
        __slots__ = (
            # Bone name, used as key in many places.
            "name",
            "parent",  # decorated bone parent, set in a later loop
            # Blender armature bone.
            "rest_bone",
            # Blender pose bone.
            "pose_bone",
            # Blender pose matrix.
            "pose_mat",
            # Blender rest matrix (armature space).
            "rest_arm_mat",
            # Blender rest matrix (local space).
            "rest_local_mat",
            # Pose_mat inverted.
            "pose_imat",
            # Rest_arm_mat inverted.
            "rest_arm_imat",
            # Rest_local_mat inverted.
            "rest_local_imat",
            # Last used euler to preserve euler compatibility in between keyframes.
            "prev_euler",
            # Is the bone disconnected to the parent bone?
            "skip_position",
            "rot_order",
            "rot_order_str",
            # Needed for the euler order when converting from a matrix.
            "rot_order_str_reverse",
        )

        _eul_order_lookup = {
            'XYZ': (0, 1, 2),
            'XZY': (0, 2, 1),
            'YXZ': (1, 0, 2),
            'YZX': (1, 2, 0),
            'ZXY': (2, 0, 1),
            'ZYX': (2, 1, 0),
        }

        def __init__(self, bone_name):
            self.name = bone_name
            self.rest_bone = arm.bones[bone_name]
            self.pose_bone = obj.pose.bones[bone_name]

            if rotate_mode == "NATIVE":
                self.rot_order_str = ensure_rot_order(self.pose_bone.rotation_mode)
            else:
                self.rot_order_str = rotate_mode
            self.rot_order_str_reverse = self.rot_order_str[::-1]

            self.rot_order = DecoratedBone._eul_order_lookup[self.rot_order_str]

            self.pose_mat = self.pose_bone.matrix

            # mat = self.rest_bone.matrix  # UNUSED
            self.rest_arm_mat = self.rest_bone.matrix_local
            self.rest_local_mat = self.rest_bone.matrix

            # inverted mats
            self.pose_imat = self.pose_mat.inverted()
            self.rest_arm_imat = self.rest_arm_mat.inverted()
            self.rest_local_imat = self.rest_local_mat.inverted()

            self.parent = None
            self.prev_euler = Euler((0.0, 0.0, 0.0), self.rot_order_str_reverse)
            # self.skip_position = ((self.rest_bone.use_connect or root_transform_only) and self.rest_bone.parent)
            self.skip_position = True

        def update_posedata(self):
            self.pose_mat = self.pose_bone.matrix
            self.pose_imat = self.pose_mat.inverted()

        def __repr__(self):
            if self.parent:
                return "[\"%s\" child on \"%s\"]\n" % (self.name, self.parent.name)
            else:
                return "[\"%s\" root bone]\n" % (self.name)

    bones_decorated = [DecoratedBone(bone_name) for bone_name in serialized_names]

    # Assign parents
    bones_decorated_dict = {dbone.name: dbone for dbone in bones_decorated}
    for dbone in bones_decorated:
        parent = dbone.rest_bone.parent
        if parent:
            dbone.parent = bones_decorated_dict[parent.name]
    del bones_decorated_dict
    # finish assigning parents

    scene = bpy.context.scene
    frame_start = scene.frame_start
    frame_end = scene.frame_end
    frame_current = scene.frame_current
    frame_count = frame_end - frame_start + 1
    frame_duration = (1.0 / (scene.render.fps / scene.render.fps_base))

    print("Frame count: %d\n" % frame_count)
    print("Frame duration: %.6f\n" % frame_duration)

    for frame in range(frame_start, frame_end + 1):
        scene.frame_set(frame)

        for dbone in bones_decorated:
            dbone.update_posedata()

        for dbone in bones_decorated:
            trans = Matrix.Translation(dbone.rest_bone.head_local)
            itrans = Matrix.Translation(-dbone.rest_bone.head_local)

            if dbone.parent:
                mat_final = dbone.parent.rest_arm_mat @ dbone.parent.pose_imat @ dbone.pose_mat @ dbone.rest_arm_imat
                mat_final = itrans @ mat_final @ trans
                loc = mat_final.to_translation() + (dbone.rest_bone.head_local - dbone.parent.rest_bone.head_local)
            else:
                mat_final = dbone.pose_mat @ dbone.rest_arm_imat
                mat_final = itrans @ mat_final @ trans
                loc = mat_final.to_translation() + dbone.rest_bone.head

            # keep eulers compatible, no jumping on interpolation.
            rot = mat_final.to_euler(dbone.rot_order_str_reverse, dbone.prev_euler)

            if not dbone.skip_position:
                values.append(round_array(loc)[:]) # location

            rt = [None, None, None]
            rt[0] = degrees(rot[dbone.rot_order[0]]) # rotation_euler
            rt[1] = degrees(rot[dbone.rot_order[1]]) # rotation_euler
            rt[2] = degrees(rot[dbone.rot_order[2]]) # rotation_euler
            values.append(round_array_no_unit_scale(rt)[:])

            dbone.prev_euler = rot

    scene.frame_set(frame_current)
    armature = obj
    numbones = len(armature.pose.bones)
    HANIM_DEF_PREFIX = 'hanim_'
    if root_found:
        print("humanoid_root found in bone data, adding position")
        channelsEnabled=MFBool([random.choice([True]) for i in range((numbones + 1) * 3)])
        channels="6 Xposition Yposition Zposition Xrotation Yrotation Zrotation "+("3 Xrotation Yrotation Zrotation " * (numbones - 1))
        joints=HANIM_DEF_PREFIX+"humanoid_root "+(" ".join(HANIM_DEF_PREFIX+bone.name for bone in armature.pose.bones if bone.name != "humanoid_root"))
    else:
        print("humanoid_root not found in bone data, not adding position")
        channelsEnabled=MFBool([random.choice([True]) for i in range(numbones * 3)])
        channels=("3 Xrotation Yrotation Zrotation " * (numbones))
        joints=(" ".join(HANIM_DEF_PREFIX+bone.name for bone in armature.pose.bones))

    node = HAnimMotion(
        frameIncrement=1,
        #  frameCount=frame_count, outputOnly
        frameIndex=frame_start,
        frameDuration=frame_duration,
        loop=True,
        enabled=True,
        channels=channels,
        joints=joints,
        channelsEnabled=channelsEnabled,
        values=MFFloat(values)
        )
    return node
