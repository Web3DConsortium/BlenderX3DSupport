# BlenderX3DSupport

# Attention
With the deployment of the Blender Extensions platform in May 2024 and the reorganization of the Blender Foundations open source code repositories, this repository, which was forked from https://github.com/blender/blender-addons , is no longer useful for development in collaboration with the larger Blender community.

Those users who have forked from this repository should evaluate whether they wih to continue to base their work on this repository. A pull-request to this repository will not be compatible with being passed on to the Blender codebase.

The positive news is that the X3D import and export code from this repository is now maintained at https://projects.blender.org/extensions/io_scene_x3d 


## Legacy README content
This purpose of this project is to support work by the X3D community to improve the  importing of X3D files into Blender and exporting Blender projects to X3D  files. This project was cloned from the Blender add-ons repository  git://git.blender.org/blender-addons.git . The Blender Add-On project page is at https://developer.blender.org/diffusion/BA/repository/master/ . The code for the X3D importer and exporter is in directory io_scene_x3d .

Contributors are invited to fork this project, develop X3D support capabilities, and present pull requests to this 
repository. This reposity is administered by the Web3D Consortium (https://www.web3d.org). Please observe these resources for Blender developers (https://wiki.blender.org/wiki/Main_Page) and a coding style guidelines (https://wiki.blender.org/wiki/Style_Guide)!

Goals to address:

1. The Blender exporter distributed with the standard Blender distribution does not support exporting X3D scenes that use image based textures. Neither texture support of X3D v3.3 nor the physically based rendering textures of X3D v4 are supported.See: https://developer.blender.org/T66534 address in simplest way possible. Specifically, get the texture URL from Blender PBR nodes, and just use it "naively" for a diffuse texture in Appearance.texture in the X3D output.

2. The exporter should generate X3D 3.3 files (with Appearance and Material nodes) and support an option for X3Dv4 Appearance model (PBR and gltf aligned)

3. Export PhysicalMaterial, export baseColor, baseTexture. As X3D v4 Materials By default already follow PBR, some code may actually get more straightforward this way. If in doubt, follow what glTF exporter does -- they already have Python code to "flatten" complicated Blender material setup using nodes -> simple PBR terms.


