# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 The x3dv-Blender-IO authors.

import bpy
from ..com.x3dv_blender_material_helpers import get_x3dv_node_name, create_settings_group

################ x3dv Material Output node ###########################################

def create_x3dv_ao_group(operator, group_name):

    # create a new group
    x3dv_ao_group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")

    return x3dv_ao_group

class NODE_OT_x3dv_SETTINGS(bpy.types.Operator):
    bl_idname = "node.x3dv_settings_node_operator"
    bl_label  = "x3dv Material Output"
    bl_description = "Add a node to the active tree for x3dv export"

    @classmethod
    def poll(cls, context):
        space = context.space_data
        return space.type == "NODE_EDITOR" \
            and context.object and context.object.active_material \
            and context.object.active_material.use_nodes is True \
            and bpy.context.preferences.addons['io_scene_x3dv'].preferences.settings_node_ui is True

    def execute(self, context):
        x3dv_settings_node_name = get_x3dv_node_name()
        if x3dv_settings_node_name in bpy.data.node_groups:
            my_group = bpy.data.node_groups[get_x3dv_node_name()]
        else:
            my_group = create_settings_group(x3dv_settings_node_name)
        node_tree = context.object.active_material.node_tree
        new_node = node_tree.nodes.new("ShaderNodeGroup")
        new_node.node_tree = bpy.data.node_groups[my_group.name]
        return {"FINISHED"}


def add_x3dv_settings_to_menu(self, context) :
    if bpy.context.preferences.addons['io_scene_x3dv'].preferences.settings_node_ui is True:
        self.layout.operator("node.x3dv_settings_node_operator")

def register():
    bpy.utils.register_class(NODE_OT_x3dv_SETTINGS)
    bpy.types.NODE_MT_category_SH_NEW_OUTPUT.append(add_x3dv_settings_to_menu)


def unregister():
    bpy.utils.unregister_class(NODE_OT_x3dv_SETTINGS)

