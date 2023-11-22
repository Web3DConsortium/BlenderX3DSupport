# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 The x3dv-Blender-IO authors.

import bpy

def get_x3dv_node_name():
    return "x3dv Material Output"

def create_settings_group(name):
    x3dv_node_group = bpy.data.node_groups.new(name, 'ShaderNodeTree')
    x3dv_node_group.inputs.new("NodeSocketFloat", "Occlusion")
    thicknessFactor  = x3dv_node_group.inputs.new("NodeSocketFloat", "Thickness")
    thicknessFactor.default_value = 0.0
    x3dv_node_group.nodes.new('NodeGroupOutput')
    x3dv_node_group_input = x3dv_node_group.nodes.new('NodeGroupInput')
    specular = x3dv_node_group.inputs.new("NodeSocketFloat", "Specular")
    specular.default_value = 1.0
    specularColor = x3dv_node_group.inputs.new("NodeSocketColor", "Specular Color")
    specularColor.default_value = [1.0,1.0,1.0,1.0]
    x3dv_node_group_input.location = -200, 0
    return x3dv_node_group
