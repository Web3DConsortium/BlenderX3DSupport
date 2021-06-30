#====================== BEGIN GPL LICENSE BLOCK ======================
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
#======================= END GPL LICENSE BLOCK ========================

# <pep8 compliant>

import bpy

from ..chain_rigs import SimpleChainRig
from ...base_rig import stage


class Rig(SimpleChainRig):
    """ A "copy_chain" rig.  All it does is duplicate the original bone chain
        and constrain it.
        This is a control and deformation rig.
    """
    def initialize(self):
        super().initialize()

        """ Gather and validate data about the rig.
        """
        self.make_controls = self.params.make_controls
        self.make_deforms = self.params.make_deforms

    ##############################
    # Control chain

    @stage.generate_bones
    def make_control_chain(self):
        if self.make_controls:
            super().make_control_chain()

    @stage.parent_bones
    def parent_control_chain(self):
        if self.make_controls:
            super().parent_control_chain()

    @stage.configure_bones
    def configure_control_chain(self):
        if self.make_controls:
            super().configure_control_chain()

    @stage.generate_widgets
    def make_control_widgets(self):
        if self.make_controls:
            super().make_control_widgets()

    ##############################
    # ORG chain

    @stage.rig_bones
    def rig_org_chain(self):
        if self.make_controls:
            super().rig_org_chain()

    ##############################
    # Deform chain

    @stage.generate_bones
    def make_deform_chain(self):
        if self.make_deforms:
            super().make_deform_chain()

    @stage.parent_bones
    def parent_deform_chain(self):
        if self.make_deforms:
            super().parent_deform_chain()

    @stage.rig_bones
    def rig_deform_chain(self):
        if self.make_deforms:
            super().rig_deform_chain()

    ##############################
    # Parameter UI

    @classmethod
    def add_parameters(self, params):
        """ Add the parameters of this rig type to the
            RigifyParameters PropertyGroup
        """
        params.make_controls = bpy.props.BoolProperty(name="Controls", default=True, description="Create control bones for the copy")
        params.make_deforms = bpy.props.BoolProperty(name="Deform", default=True, description="Create deform bones for the copy")

    @classmethod
    def parameters_ui(self, layout, params):
        """ Create the ui for the rig parameters.
        """
        r = layout.row()
        r.prop(params, "make_controls")
        r = layout.row()
        r.prop(params, "make_deforms")


def create_sample(obj):
    """ Create a sample metarig for this rig type.
    """
    # generated by rigify.utils.write_metarig
    bpy.ops.object.mode_set(mode='EDIT')
    arm = obj.data

    bones = {}

    bone = arm.edit_bones.new('bone.01')
    bone.head[:] = 0.0000, 0.0000, 0.0000
    bone.tail[:] = 0.0000, 0.0000, 0.3333
    bone.roll = 0.0000
    bone.use_connect = False
    bones['bone.01'] = bone.name
    bone = arm.edit_bones.new('bone.02')
    bone.head[:] = 0.0000, 0.0000, 0.3333
    bone.tail[:] = 0.0000, 0.0000, 0.6667
    bone.roll = 3.1416
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['bone.01']]
    bones['bone.02'] = bone.name
    bone = arm.edit_bones.new('bone.03')
    bone.head[:] = 0.0000, 0.0000, 0.6667
    bone.tail[:] = 0.0000, 0.0000, 1.0000
    bone.roll = 3.1416
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['bone.02']]
    bones['bone.03'] = bone.name

    bpy.ops.object.mode_set(mode='OBJECT')
    pbone = obj.pose.bones[bones['bone.01']]
    pbone.rigify_type = 'basic.copy_chain'
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['bone.02']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['bone.03']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'

    bpy.ops.object.mode_set(mode='EDIT')
    for bone in arm.edit_bones:
        bone.select = False
        bone.select_head = False
        bone.select_tail = False
    for b in bones:
        bone = arm.edit_bones[bones[b]]
        bone.select = True
        bone.select_head = True
        bone.select_tail = True
        arm.edit_bones.active = bone

    return bones
