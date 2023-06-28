# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 The x3dv-Blender-IO authors.

# https://wiki.blender.org/wiki/Process/Addons/Guidelines/metainfo
bl_info = {
    'name': 'Web3D X3DV format',
    'author': ', and many external contributors',
    "version": (3, 5, 0),
    'blender': (3, 5, 0),
    'location': 'File > Import-Export',
    'description': 'Import-Export x3d, x3dv, json, html',
    'warning': '',
    'doc_url': "{BLENDER_MANUAL_URL}/addons/import_export/scene_x3dv.html",
    'tracker_url': "https://github.com/????/x3d-Blender-IO/issues/",
    'support': 'COMMUNITY',  # 'OFFICIAL'
    'category': 'Import-Export',
}

def get_version_string():
    return str(bl_info['version'][0]) + '.' + str(bl_info['version'][1]) + '.' + str(bl_info['version'][2])

#
# Script reloading (if the user calls 'Reload Scripts' from Blender)
#

def reload_package(module_dict_main):
    import importlib
    from pathlib import Path

    def reload_package_recursive(current_dir, module_dict):
        for path in current_dir.iterdir():
            if "__init__" in str(path) or path.stem not in module_dict:
                continue

            if path.is_file() and path.suffix == ".py":
                importlib.reload(module_dict[path.stem])
            elif path.is_dir():
                reload_package_recursive(path, module_dict[path.stem].__dict__)

    reload_package_recursive(Path(__file__).parent, module_dict_main)


if "bpy" in locals():
    reload_package(locals())

import bpy
from bpy.props import (StringProperty,
                       BoolProperty,
                       EnumProperty,
                       IntProperty,
                       CollectionProperty)
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper, ExportHelper


#
#  Functions / Classes.
#

exporter_extension_panel_unregister_functors = []
importer_extension_panel_unregister_functors = []


def ensure_filepath_matches_export_format(filepath, export_format):
    import os
    filename = os.path.basename(filepath)
    if not filename:
        return filepath

    stem, ext = os.path.splitext(filename)
    if stem.startswith('.') and not ext:
        stem, ext = '', stem

    desired_ext = '.x3d' if export_format == 'X3D' else '.x3dv' if export_format == 'VRML' else '.html' if export_format == 'HTML' else '.json'
    ext_lower = ext.lower()
    if ext_lower not in ['.x3d', '.x3dv', '.html', '.json']:
        return filepath + desired_ext
    elif ext_lower != desired_ext:
        filepath = filepath[:-len(ext)]  # strip off ext
        return filepath + desired_ext
    else:
        return filepath


def on_export_format_changed(self, context):
    # Update the filename in the file browser when the format (.x3d/.x3dv/.html/.json)
    # changes
    sfile = context.space_data
    if not isinstance(sfile, bpy.types.SpaceFileBrowser):
        return
    if not sfile.active_operator:
        return
    if sfile.active_operator.bl_idname != "EXPORT_SCENE_OT_x3d":
        return

    sfile.params.filename = ensure_filepath_matches_export_format(
        sfile.params.filename,
        self.export_format,
    )

    # Also change the filter
    sfile.params.filter_glob = '*.x3d' if export_format == 'X3D' else '*.x3dv' if export_format == 'VRML' else '*.html' if export_format == 'HTML' else '*.json'
    # Force update of file list, has update the filter does not update the real file list
    bpy.ops.file.refresh()


class ConvertX3DV_Base:
    """Base class containing options that should be exposed during both import and export."""

    convert_lighting_mode: EnumProperty(
        name='Lighting Mode',
        items=(
            ('SPEC', 'Standard', 'Physically-based lighting units (cd, lx, nt)'),
            ('COMPAT', 'Unitless', 'Non-physical, unitless lighting. Useful when exposure controls are not available'),
            ('RAW', 'Raw (Deprecated)', 'Blender lighting strengths with no conversion'),
        ),
        description='Optional backwards compatibility for non-standard render engines. Applies to lights',# TODO: and emissive materials',
        default='SPEC'
    )

class ExportX3DV_Base(ConvertX3DV_Base):
    # TODO: refactor to avoid boilerplate

    def __init__(self):
        pass

    bl_options = {'PRESET'}

    # Don't use export_ prefix here, I don't want it to be saved with other export settings
    x3dv_export_id: StringProperty(
        name='Identifier',
        description=(
            'Identifier of caller (in case of add-on calling this exporter). '
            'Can be useful in case of Extension added by other add-ons'
        ),
        default=''
    )

    export_format: EnumProperty(
        name='Format',
        items=(('X3D', 'x3d (.x3d)','Exports xml style x3d. '),
               ('VRML', 'x3dv (.x3dv)','vrml2  wrl style '),
               ('HTML', 'html (.html)','xml style in html'),
               ('JSON', 'json (.json)','json style')),
        description=(
            'Output format options. '),
        default='X3D', #Warning => If you change the default, need to change the default filter too
        update=on_export_format_changed,
    )

    ui_tab: EnumProperty(
        items=(('GENERAL', "General", "General settings"),
               ('MESHES', "Meshes", "Mesh settings"),
               ('OBJECTS', "Objects", "Object settings"),
               ('ANIMATION', "Animation", "Animation settings")),
        name="ui_tab",
        description="Export setting categories",
    )

    export_copyright: StringProperty(
        name='Copyright',
        description='Legal rights and conditions for the model',
        default=''
    )

    export_image_format: EnumProperty(
        name='Images',
        items=(('AUTO', 'Automatic',
                'Save PNGs as PNGs and JPEGs as JPEGs. '
                'If neither one, use PNG'),
                ('JPEG', 'JPEG Format (.jpg)',
                'Save images as JPEGs. (Images that need alpha are saved as PNGs though.) '
                'Be aware of a possible loss in quality'),
                ('NONE', 'None',
                 'Don\'t export images'),
               ),
        description=(
            'Output format for images. PNG is lossless and generally preferred, but JPEG might be preferable for web '
            'applications due to the smaller file size. Alternatively they can be omitted if they are not needed'
        ),
        default='AUTO'
    )

    export_texture_dir: StringProperty(
        name='Textures',
        description='Folder to place texture files in. Relative to the .x3dv file',
        default='',
    )

    export_jpeg_quality: IntProperty(
        name='JPEG quality',
        description='Quality of JPEG export',
        default=75,
        min=0,
        max=100
    )

    export_keep_originals: BoolProperty(
        name='Keep original',
        description=('Keep original textures files if possible. '
                     'WARNING: if you use more than one texture, '
                     'where pbr standard requires only one, only one texture will be used. '
                     'This can lead to unexpected results'
        ),
        default=False,
    )

    export_texcoords: BoolProperty(
        name='UVs',
        description='Export UVs (texture coordinates) with meshes',
        default=True
    )

    export_normals: BoolProperty(
        name='Normals',
        description='Export vertex normals with meshes',
        default=False
    )

    export_tangents: BoolProperty(
        name='Tangents',
        description='Export vertex tangents with meshes',
        default=False
    )

    export_materials: EnumProperty(
        name='Materials',
        items=(('EXPORT', 'Export',
        'Export all materials used by included objects'),
        ('PLACEHOLDER', 'Placeholder',
        'Do not export materials, but write multiple primitive groups per mesh, keeping material slot information'),
        ('NONE', 'No export',
        'Do not export materials, and combine mesh primitive groups, losing material slot information')),
        description='Export materials',
        default='EXPORT'
    )


    export_original_specular: BoolProperty(
        name='Export original PBR Specular',
        description=(
            'Export original x3dv PBR Specular, instead of Blender Principled Shader Specular'
        ),
        default=False,
    )

    export_colors: BoolProperty(
        name='Vertex Colors',
        description='Export vertex colors with meshes',
        default=False
    )

    export_attributes: BoolProperty(
        name='Attributes',
        description='Export Attributes (when starting with underscore)',
        default=False
    )

    use_mesh_edges: BoolProperty(
        name='Loose Edges',
        description=(
            'Export loose edges as lines, using the material from the first material slot'
        ),
        default=False,
    )

    use_mesh_vertices: BoolProperty(
        name='Loose Points',
        description=(
            'Export loose points as x3dv points, using the material from the first material slot'
        ),
        default=False,
    )

    export_cameras: BoolProperty(
        name='Cameras',
        description='Export cameras',
        default=True
    )

    use_selection: BoolProperty(
        name='Selected Objects',
        description='Export selected objects only',
        default=False
    )

    use_visible: BoolProperty(
        name='Visible Objects',
        description='Export visible objects only',
        default=False
    )

    use_renderable: BoolProperty(
        name='Renderable Objects',
        description='Export renderable objects only',
        default=False
    )

    use_active_collection_with_nested: BoolProperty(
        name='Include Nested Collections',
        description='Include active collection and nested collections',
        default=True
    )

    use_active_collection: BoolProperty(
        name='Active Collection',
        description='Export objects in the active collection only',
        default=False
    )

    use_active_scene: BoolProperty(
        name='Active Scene',
        description='Export active scene only',
        default=False
    )

    export_extras: BoolProperty(
        name='Custom Properties',
        description='Export custom properties as x3dv metadata',
        default=False
    )

    export_yup: BoolProperty(
        name='+Y Up',
        description='Export using x3dv convention, +Y up',
        default=True
    )

    export_apply: BoolProperty(
        name='Apply Modifiers',
        description='Apply modifiers (excluding Armatures) to mesh objects -'
                    'WARNING: prevents exporting shape keys',
        default=False
    )

    export_animations: BoolProperty(
        name='Animations',
        description='Exports active actions and NLA tracks as x3dv animations',
        default=True
    )

    export_frame_range: BoolProperty(
        name='Limit to Playback Range',
        description='Clips animations to selected playback range',
        default=True
    )

    export_frame_step: IntProperty(
        name='Sampling Rate',
        description='How often to evaluate animated values (in frames)',
        default=1,
        min=1,
        max=120
    )

    export_force_sampling: BoolProperty(
        name='Always Sample Animations',
        description='Apply sampling to all animations',
        default=True
    )

    export_nla_strips: BoolProperty(
        name='Group by NLA Track',
        description=(
            "When on, multiple actions become part of the same x3dv animation if "
            "they're pushed onto NLA tracks with the same name. "
            "When off, all the currently assigned actions become one x3dv animation"
        ),
        default=True
    )

    export_nla_strips_merged_animation_name: StringProperty(
        name='Merged Animation Name',
        description=(
            "Name of single x3dv animation to be exported"
        ),
        default='Animation'
    )

    export_def_bones: BoolProperty(
        name='Export Deformation Bones Only',
        description='Export Deformation bones only',
        default=False
    )

    export_optimize_animation_size: BoolProperty(
        name='Optimize Animation Size',
        description=(
            "Reduce exported file size by removing duplicate keyframes "
            "(can cause problems with stepped animation)"
        ),
        default=False
    )

    export_anim_single_armature: BoolProperty(
        name='Export all Armature Actions',
        description=(
            "Export all actions, bound to a single armature. "
            "WARNING: Option does not support exports including multiple armatures"
        ),
        default=True
    )

    export_reset_pose_bones: BoolProperty(
        name='Reset pose bones between actions',
        description=(
            "Reset pose bones between each action exported. "
            "This is needed when some bones are not keyed on some animations"
        ),
        default=True
    )

    export_current_frame: BoolProperty(
        name='Use Current Frame',
        description='Export the scene in the current animation frame',
        default=False
    )

    export_skins: BoolProperty(
        name='Skinning',
        description='Export skinning (armature) data',
        default=True
    )

    export_all_influences: BoolProperty(
        name='Include All Bone Influences',
        description='Allow >4 joint vertex influences. Models may appear incorrectly in many viewers',
        default=False
    )

    export_morph: BoolProperty(
        name='Shape Keys',
        description='Export shape keys (morph targets)',
        default=True
    )

    export_morph_normal: BoolProperty(
        name='Shape Key Normals',
        description='Export vertex normals with shape keys (morph targets)',
        default=True
    )

    export_morph_tangent: BoolProperty(
        name='Shape Key Tangents',
        description='Export vertex tangents with shape keys (morph targets)',
        default=False
    )

    export_lights: BoolProperty(
        name='Punctual Lights',
        description='Export directional, point, and spot lights. ',
        default=False
    )

    will_save_settings: BoolProperty(
        name='Remember Export Settings',
        description='Store x3dv export settings in the Blender project',
        default=False)

    # Custom scene property for saving settings
    scene_key = "x3dvExportSettings"

    #

    def check(self, _context):
        # Ensure file extension matches format
        old_filepath = self.filepath
        self.filepath = ensure_filepath_matches_export_format(
            self.filepath,
            self.export_format,
        )
        return self.filepath != old_filepath

    def invoke(self, context, event):
        settings = context.scene.get(self.scene_key)
        self.will_save_settings = False
        if settings:
            try:
                for (k, v) in settings.items():
                    setattr(self, k, v)
                self.will_save_settings = True

            except (AttributeError, TypeError):
                self.report({"ERROR"}, "Loading export settings failed. Removed corrupted settings")
                del context.scene[self.scene_key]

        import sys
        preferences = bpy.context.preferences
        for addon_name in preferences.addons.keys():
            try:
                if hasattr(sys.modules[addon_name], 'x3dvExportUserExtension') or hasattr(sys.modules[addon_name], 'x3dvExportUserExtensions'):
                    exporter_extension_panel_unregister_functors.append(sys.modules[addon_name].register_panel())
            except Exception:
                pass

        self.has_active_exporter_extensions = len(exporter_extension_panel_unregister_functors) > 0
        return ExportHelper.invoke(self, context, event)

    def save_settings(self, context):
        # find all props to save
        exceptional = [
            # options that don't start with 'export_'
            'use_selection',
            'use_visible',
            'use_renderable',
            'use_active_collection_with_nested',
            'use_active_collection',
            'use_mesh_edges',
            'use_mesh_vertices',
            'use_active_scene',
        ]
        all_props = self.properties
        export_props = {
            x: getattr(self, x) for x in dir(all_props)
            if (x.startswith("export_") or x in exceptional) and all_props.get(x) is not None
        }
        context.scene[self.scene_key] = export_props

    def execute(self, context):
        import os
        import datetime
        from .blender.exp import x3dv_blender_export
        from .io.com.x3dv_io_path import path_to_uri

        if self.will_save_settings:
            self.save_settings(context)

        self.check(context)  # ensure filepath has the right extension

        # All custom export settings are stored in this container.
        export_settings = {}
        # no menu items yet for these >>
        export_settings['x3dv_use_triangulate'] = False
        export_settings['x3dv_use_compress'] = False
        export_settings['x3dv_use_hierarchy'] = True
        export_settings['x3dv_name_decorations'] = True
        export_settings['x3dv_blender_file'] = bpy.data.filepath
        export_settings['x3dv_blender_directory'] = os.path.dirname(bpy.data.filepath)
        export_settings['x3dv_use_mesh_modifiers'] = False
        # << no menu items yet 

        export_settings['timestamp'] = datetime.datetime.now()
        export_settings['x3dv_export_id'] = self.x3dv_export_id
        export_settings['x3dv_filepath'] = self.filepath
        export_settings['x3dv_filedirectory'] = os.path.dirname(export_settings['x3dv_filepath']) + '/'
        export_settings['x3dv_texturedirectory'] = os.path.join(
            export_settings['x3dv_filedirectory'],
            self.export_texture_dir,
        )
        export_settings['x3dv_keep_original_textures'] = self.export_keep_originals

        export_settings['x3dv_format'] = self.export_format
        export_settings['x3dv_image_format'] = self.export_image_format
        export_settings['x3dv_jpeg_quality'] = self.export_jpeg_quality
        export_settings['x3dv_copyright'] = self.export_copyright
        export_settings['x3dv_texcoords'] = self.export_texcoords
        export_settings['x3dv_normals'] = self.export_normals
        export_settings['x3dv_tangents'] = self.export_tangents and self.export_normals
        export_settings['x3dv_loose_edges'] = self.use_mesh_edges
        export_settings['x3dv_loose_points'] = self.use_mesh_vertices


        export_settings['x3dv_materials'] = self.export_materials
        export_settings['x3dv_colors'] = self.export_colors
        export_settings['x3dv_attributes'] = self.export_attributes
        export_settings['x3dv_cameras'] = self.export_cameras

        export_settings['x3dv_original_specular'] = self.export_original_specular

        export_settings['x3dv_visible'] = self.use_visible
        export_settings['x3dv_renderable'] = self.use_renderable

        export_settings['x3dv_active_collection'] = self.use_active_collection
        if self.use_active_collection:
            export_settings['x3dv_active_collection_with_nested'] = self.use_active_collection_with_nested
        else:
            export_settings['x3dv_active_collection_with_nested'] = False
        export_settings['x3dv_active_scene'] = self.use_active_scene

        export_settings['x3dv_selected'] = self.use_selection
        export_settings['x3dv_layers'] = True  # self.export_layers
        export_settings['x3dv_extras'] = self.export_extras
        export_settings['x3dv_yup'] = self.export_yup
        export_settings['x3dv_apply'] = self.export_apply
        export_settings['x3dv_current_frame'] = self.export_current_frame
        export_settings['x3dv_animations'] = self.export_animations
        export_settings['x3dv_def_bones'] = self.export_def_bones
        if self.export_animations:
            export_settings['x3dv_frame_range'] = self.export_frame_range
            export_settings['x3dv_force_sampling'] = self.export_force_sampling
            if not self.export_force_sampling:
                export_settings['x3dv_def_bones'] = False
            export_settings['x3dv_nla_strips'] = self.export_nla_strips
            export_settings['x3dv_nla_strips_merged_animation_name'] = self.export_nla_strips_merged_animation_name
            export_settings['x3dv_optimize_animation'] = self.export_optimize_animation_size
            export_settings['x3dv_export_anim_single_armature'] = self.export_anim_single_armature
            export_settings['x3dv_export_reset_pose_bones'] = self.export_reset_pose_bones
        else:
            export_settings['x3dv_frame_range'] = False
            export_settings['x3dv_move_keyframes'] = False
            export_settings['x3dv_force_sampling'] = False
            export_settings['x3dv_optimize_animation'] = False
            export_settings['x3dv_export_anim_single_armature'] = False
            export_settings['x3dv_export_reset_pose_bones'] = False
        export_settings['x3dv_skins'] = self.export_skins
        if self.export_skins:
            export_settings['x3dv_all_vertex_influences'] = self.export_all_influences
        else:
            export_settings['x3dv_all_vertex_influences'] = False
            export_settings['x3dv_def_bones'] = False
        export_settings['x3dv_frame_step'] = self.export_frame_step
        export_settings['x3dv_morph'] = self.export_morph
        if self.export_morph:
            export_settings['x3dv_morph_normal'] = self.export_morph_normal
        else:
            export_settings['x3dv_morph_normal'] = False
        if self.export_morph and self.export_morph_normal:
            export_settings['x3dv_morph_tangent'] = self.export_morph_tangent
        else:
            export_settings['x3dv_morph_tangent'] = False

        export_settings['x3dv_lights'] = self.export_lights
        export_settings['x3dv_lighting_mode'] = self.convert_lighting_mode

        #export_settings['x3dv_binary'] = bytearray()
        #export_settings['x3dv_binaryfilename'] = (
        #    path_to_uri(os.path.splitext(os.path.basename(self.filepath))[0] + '.bin')
        #)

        return x3dv_blender_export.save(context, export_settings)

    def draw(self, context):
        pass # Is needed to get panels available


class X3DV_PT_export_main(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = ""
    bl_parent_id = "FILE_PT_operator"
    bl_options = {'HIDE_HEADER'}

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator

        return operator.bl_idname == "EXPORT_SCENE_OT_x3dv"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        sfile = context.space_data
        operator = sfile.active_operator

        layout.prop(operator, 'export_format')
        layout.prop(operator, 'export_keep_originals')
        if operator.export_keep_originals is False:
            layout.prop(operator, 'export_texture_dir', icon='FILE_FOLDER')

        layout.prop(operator, 'export_copyright')
        layout.prop(operator, 'will_save_settings')


class X3DV_PT_export_include(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "Include"
    bl_parent_id = "FILE_PT_operator"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator

        return operator.bl_idname == "EXPORT_SCENE_OT_x3dv"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        sfile = context.space_data
        operator = sfile.active_operator

        col = layout.column(heading = "Limit to", align = True)
        col.prop(operator, 'use_selection')
        col.prop(operator, 'use_visible')
        col.prop(operator, 'use_renderable')
        col.prop(operator, 'use_active_collection')
        if operator.use_active_collection:
            col.prop(operator, 'use_active_collection_with_nested')
        col.prop(operator, 'use_active_scene')

        col = layout.column(heading = "Data", align = True)
        col.prop(operator, 'export_extras')
        col.prop(operator, 'export_cameras')
        col.prop(operator, 'export_lights')


class X3DV_PT_export_transform(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "Transform"
    bl_parent_id = "FILE_PT_operator"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator

        return operator.bl_idname == "EXPORT_SCENE_OT_x3dv"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        sfile = context.space_data
        operator = sfile.active_operator

        layout.prop(operator, 'export_yup')


class X3DV_PT_export_geometry(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "Data"
    bl_parent_id = "FILE_PT_operator"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator

        return operator.bl_idname == "EXPORT_SCENE_OT_x3dv"

    def draw(self, context):
        pass

class X3DV_PT_export_geometry_mesh(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "Mesh"
    bl_parent_id = "X3DV_PT_export_geometry"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator
        return operator.bl_idname == "EXPORT_SCENE_OT_x3dv"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        sfile = context.space_data
        operator = sfile.active_operator

        layout.prop(operator, 'export_apply')
        layout.prop(operator, 'export_texcoords')
        layout.prop(operator, 'export_normals')
        col = layout.column()
        col.active = operator.export_normals
        col.prop(operator, 'export_tangents')
        layout.prop(operator, 'export_colors')
        layout.prop(operator, 'export_attributes')

        col = layout.column()
        col.prop(operator, 'use_mesh_edges')
        col.prop(operator, 'use_mesh_vertices')


class X3DV_PT_export_geometry_material(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "Material"
    bl_parent_id = "X3DV_PT_export_geometry"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator
        return operator.bl_idname == "EXPORT_SCENE_OT_x3dv"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        sfile = context.space_data
        operator = sfile.active_operator

        layout.prop(operator, 'export_materials')
        col = layout.column()
        col.active = operator.export_materials == "EXPORT"
        col.prop(operator, 'export_image_format')
        if operator.export_image_format in ["AUTO", "JPEG"]:
            col.prop(operator, 'export_jpeg_quality')

class X3DV_PT_export_geometry_original_pbr(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "PBR Extensions"
    bl_parent_id = "X3DV_PT_export_geometry_material"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator
        return operator.bl_idname == "EXPORT_SCENE_OT_x3dv"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        sfile = context.space_data
        operator = sfile.active_operator

        layout.prop(operator, 'export_original_specular')

class X3DV_PT_export_geometry_lighting(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "Lighting"
    bl_parent_id = "X3DV_PT_export_geometry"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator
        return operator.bl_idname == "EXPORT_SCENE_OT_x3dv"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        sfile = context.space_data
        operator = sfile.active_operator

        layout.prop(operator, 'convert_lighting_mode')


class X3DV_PT_export_animation(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "Animation"
    bl_parent_id = "FILE_PT_operator"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator

        return operator.bl_idname == "EXPORT_SCENE_OT_x3dv"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        sfile = context.space_data
        operator = sfile.active_operator

        layout.prop(operator, 'export_current_frame')


class X3DV_PT_export_animation_export(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "Animation"
    bl_parent_id = "X3DV_PT_export_animation"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator

        return operator.bl_idname == "EXPORT_SCENE_OT_x3dv"

    def draw_header(self, context):
        sfile = context.space_data
        operator = sfile.active_operator
        self.layout.prop(operator, "export_animations", text="")

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        sfile = context.space_data
        operator = sfile.active_operator

        layout.active = operator.export_animations

        layout.prop(operator, 'export_frame_range')
        layout.prop(operator, 'export_frame_step')
        layout.prop(operator, 'export_force_sampling')
        layout.prop(operator, 'export_nla_strips')
        if operator.export_nla_strips is False:
            layout.prop(operator, 'export_nla_strips_merged_animation_name')
        layout.prop(operator, 'export_optimize_animation_size')
        layout.prop(operator, 'export_anim_single_armature')
        layout.prop(operator, 'export_reset_pose_bones')


class X3DV_PT_export_animation_shapekeys(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "Shape Keys"
    bl_parent_id = "X3DV_PT_export_animation"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator

        return operator.bl_idname == "EXPORT_SCENE_OT_x3dv"

    def draw_header(self, context):
        sfile = context.space_data
        operator = sfile.active_operator
        self.layout.prop(operator, "export_morph", text="")

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        sfile = context.space_data
        operator = sfile.active_operator

        layout.active = operator.export_morph

        layout.prop(operator, 'export_morph_normal')
        col = layout.column()
        col.active = operator.export_morph_normal
        col.prop(operator, 'export_morph_tangent')


class X3DV_PT_export_animation_skinning(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "Skinning"
    bl_parent_id = "X3DV_PT_export_animation"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator

        return operator.bl_idname == "EXPORT_SCENE_OT_x3dv"

    def draw_header(self, context):
        sfile = context.space_data
        operator = sfile.active_operator
        self.layout.prop(operator, "export_skins", text="")

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        sfile = context.space_data
        operator = sfile.active_operator

        layout.active = operator.export_skins
        layout.prop(operator, 'export_all_influences')

        row = layout.row()
        row.active = operator.export_force_sampling
        row.prop(operator, 'export_def_bones')
        if operator.export_force_sampling is False and operator.export_def_bones is True:
            layout.label(text="Export only deformation bones is not possible when not sampling animation")

class ExportX3DV(bpy.types.Operator, ExportX3DV_Base, ExportHelper):
    """Export scene as x3dv file"""
    bl_idname = 'export_scene.x3dv'
    bl_label = 'Export x3dv '

    filename_ext = ''

    filter_glob: StringProperty(default='*.x3dv', options={'HIDDEN'})


def menu_func_export(self, context):
    self.layout.operator(ExportX3DV.bl_idname, text='x3dv (.x3d/.x3dv/.html/.json)')


class ImportX3DV(Operator, ConvertX3DV_Base, ImportHelper):
    """Load a x3dv file"""
    bl_idname = 'import_scene.x3dv'
    bl_label = 'Import x3dv'
    bl_options = {'REGISTER', 'UNDO'}

    filter_glob: StringProperty(default="*.x3d;*.x3dv;*.wrl;*.html;*.json", options={'HIDDEN'})

    files: CollectionProperty(
        name="File Path",
        type=bpy.types.OperatorFileListElement,
    )

    loglevel: IntProperty(
        name='Log Level',
        description="Log Level")

    import_pack_images: BoolProperty(
        name='Pack Images',
        description='Pack all images into .blend file',
        default=True
    )

    merge_vertices: BoolProperty(
        name='Merge Vertices',
        description=(
            'The x3dv format requires discontinuous normals, UVs, and '
            'other vertex attributes to be stored as separate vertices, '
            'as required for rendering on typical graphics hardware. '
            'This option attempts to combine co-located vertices where possible. '
            'Currently cannot combine verts with different normals'
        ),
        default=False,
    )

    import_shading: EnumProperty(
        name="Shading",
        items=(("NORMALS", "Use Normal Data", ""),
               ("FLAT", "Flat Shading", ""),
               ("SMOOTH", "Smooth Shading", "")),
        description="How normals are computed during import",
        default="NORMALS")

    bone_heuristic: EnumProperty(
        name="Bone Dir",
        items=(
            ("BLENDER", "Blender (best for re-importing)",
                "Good for re-importing x3dvs exported from Blender. "
                "Bone tips are placed on their local +Y axis (in x3dv space)"),
            ("TEMPERANCE", "Temperance (average)",
                "Decent all-around strategy. "
                "A bone with one child has its tip placed on the local axis "
                "closest to its child"),
            ("FORTUNE", "Fortune (may look better, less accurate)",
                "Might look better than Temperance, but also might have errors. "
                "A bone with one child has its tip placed at its child's root. "
                "Non-uniform scalings may get messed up though, so beware"),
        ),
        description="Heuristic for placing bones. Tries to make bones pretty",
        default="TEMPERANCE",
    )

    guess_original_bind_pose: BoolProperty(
        name='Guess Original Bind Pose',
        description=(
            'Try to guess the original bind pose for skinned meshes from '
            'the inverse bind matrices. '
            'When off, use default/rest pose as bind pose'
        ),
        default=True,
    )

    def draw(self, context):
        layout = self.layout

        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        layout.prop(self, 'import_pack_images')
        layout.prop(self, 'merge_vertices')
        layout.prop(self, 'import_shading')
        layout.prop(self, 'guess_original_bind_pose')
        layout.prop(self, 'bone_heuristic')
        layout.prop(self, 'convert_lighting_mode')

    def invoke(self, context, event):
        import sys

        self.has_active_importer_extensions = False
        return ImportHelper.invoke(self, context, event)

    def execute(self, context):
        return self.import_x3dv(context)

    def import_x3dv(self, context):
        import os

        self.set_debug_log()
        import_settings = self.as_keywords()

        user_extensions = []

        import sys

        if self.files:
            # Multiple file import
            ret = {'CANCELLED'}
            dirname = os.path.dirname(self.filepath)
            for file in self.files:
                path = os.path.join(dirname, file.name)
                if self.unit_import(path, import_settings) == {'FINISHED'}:
                    ret = {'FINISHED'}
            return ret
        else:
            # Single file import
            return self.unit_import(self.filepath, import_settings)

    def unit_import(self, filename, import_settings):
        import time
        from .io.imp.x3dv_io_x3dv import x3dvImporter, ImportError
        from .blender.imp.x3dv_blender_x3dv import Blenderx3dv

        try:
            x3dv_importer = x3dvImporter(filename, import_settings)
            x3dv_importer.read()
            x3dv_importer.checks()

            print("Data are loaded, start creating Blender stuff")

            start_time = time.time()
            Blenderx3dv.create(x3dv_importer)
            elapsed_s = "{:.2f}s".format(time.time() - start_time)
            print("x3dv import finished in " + elapsed_s)

            x3dv_importer.log.removeHandler(x3dv_importer.log_handler)

            return {'FINISHED'}

        except ImportError as e:
            self.report({'ERROR'}, e.args[0])
            return {'CANCELLED'}

    def set_debug_log(self):
        import logging
        if bpy.app.debug_value == 0:
            self.loglevel = logging.CRITICAL
        elif bpy.app.debug_value == 1:
            self.loglevel = logging.ERROR
        elif bpy.app.debug_value == 2:
            self.loglevel = logging.WARNING
        elif bpy.app.debug_value == 3:
            self.loglevel = logging.INFO
        else:
            self.loglevel = logging.NOTSET


def menu_func_import(self, context):
    self.layout.operator(ImportX3DV.bl_idname, text='x3dv (.x3d/.x3dv/.html/.json)')


classes = (
    ExportX3DV,
    X3DV_PT_export_main,
    X3DV_PT_export_include,
    X3DV_PT_export_transform,
    X3DV_PT_export_geometry,
    X3DV_PT_export_geometry_mesh,
    X3DV_PT_export_geometry_material,
    X3DV_PT_export_geometry_original_pbr,
    X3DV_PT_export_geometry_lighting,
    X3DV_PT_export_animation,
    X3DV_PT_export_animation_export,
    X3DV_PT_export_animation_shapekeys,
    X3DV_PT_export_animation_skinning,
    ImportX3DV,
)


def register():
    import io_scene_x3dv.blender.com.x3dv_blender_ui as blender_ui
    for c in classes:
        bpy.utils.register_class(c)
    # bpy.utils.register_module(__name__)

    blender_ui.register()

    # add to the export / import menu
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    import io_scene_x3dv.blender.com.x3dv_blender_ui as blender_ui
    blender_ui.unregister()

    for c in classes:
        bpy.utils.unregister_class(c)
    for f in exporter_extension_panel_unregister_functors:
        f()
    exporter_extension_panel_unregister_functors.clear()

    for f in importer_extension_panel_unregister_functors:
        f()
    importer_extension_panel_unregister_functors.clear()

    # bpy.utils.unregister_module(__name__)

    # remove from the export / import menu
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
