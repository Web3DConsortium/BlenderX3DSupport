# SPDX-FileCopyrightText: 2022-2023 Blender Foundation
#
# SPDX-License-Identifier: GPL-2.0-or-later

# ##### BEGIN AUTOGENERATED I18N SECTION #####
# NOTE: You can safely move around this auto-generated block (with the begin/end markers!),
#       and edit the translations by hand.
#       Just carefully respect the format of the tuple!

# Tuple of tuples:
# ((msgctxt, msgid), (sources, gen_comments), (lang, translation, (is_fuzzy, comments)), ...)
translations_tuple = (
    (("*", ""),
     ((), ()),
     ("fr_FR", "Project-Id-Version: Sun Position 3.3.3 (0)\n",
               (False,
                ("Blender's translation file (po format).",
                 "Copyright (C) 2022 The Blender Foundation.",
                 "This file is distributed under the same license as the Blender package.",
                 "Damien Picard <dam.pic@free.fr>, 2022."))),
    ),
    (("*", "Azimuth and Elevation Info"),
     (("bpy.types.SunPosAddonPreferences.show_az_el",),
      ()),
     ("fr_FR", "Infos d’azimut et de hauteur",
               (False, ())),
    ),
    (("*", "Show azimuth and solar elevation info"),
     (("bpy.types.SunPosAddonPreferences.show_az_el",),
      ()),
     ("fr_FR", "Afficher les infos d’azimut et de hauteur du Soleil",
               (False, ())),
    ),
    (("*", "Daylight Savings"),
     (("bpy.types.SunPosProperties.use_daylight_savings"),
      ()),
     ("fr_FR", "Heure d’été",
               (False, ())),
    ),
    (("*", "Display overlays in the viewport: the direction of the north, analemmas and the Sun surface"),
     (("bpy.types.SunPosAddonPreferences.show_overlays",),
      ()),
     ("fr_FR", "Afficher des surimpressions dans la vue 3D : la direction du nord, les analemmes et la surface du Soleil",
               (False, ())),
    ),
    (("*", "Refraction"),
     (("bpy.types.SunPosAddonPreferences.show_refraction",
       "scripts/addons/sun_position/ui_sun.py:151"),
      ()),
     ("fr_FR", "Réfraction",
               (False, ())),
    ),
    (("*", "Show Sun Refraction choice"),
     (("bpy.types.SunPosAddonPreferences.show_refraction",),
      ()),
     ("fr_FR", "Afficher l’option de réfraction du Soleil",
               (False, ())),
    ),
    (("*", "Sunrise and Sunset Info"),
     (("bpy.types.SunPosAddonPreferences.show_rise_set",),
      ()),
     ("fr_FR", "Infos de lever et coucher",
               (False, ())),
    ),
    (("*", "Show sunrise and sunset labels"),
     (("bpy.types.SunPosAddonPreferences.show_rise_set",),
      ()),
     ("fr_FR", "Afficher les informations de lever et coucher du Soleil",
               (False, ())),
    ),
    (("*", "Sun Position"),
     (("bpy.types.Scene.sun_pos_properties",
       "bpy.types.SUNPOS_PT_Panel",
       "Add-on Sun Position info: name"),
      ()),
     ("fr_FR", "Position du Soleil",
               (False, ())),
    ),
    (("*", "Sun Position Settings"),
     (("bpy.types.Scene.sun_pos_properties",),
      ()),
     ("fr_FR", "Options de position du Soleil",
               (False, ())),
    ),
    (("*", "Sun Position Presets"),
     (("bpy.types.SUNPOS_PT_Presets",),
      ()),
     ("fr_FR", "Préréglages de position du Soleil",
               (False, ())),
    ),
    (("Operator", "Pick Sun in Viewport"),
     (("bpy.types.WORLD_OT_sunpos_show_hdr",),
      ()),
     ("fr_FR", "Pointer le Soleil dans la vue",
               (False, ())),
    ),
    (("*", "Select the location of the Sun in any 3D viewport and keep it in sync with the environment"),
     (("bpy.types.WORLD_OT_sunpos_show_hdr",),
      ()),
     ("fr_FR", "Sélectionner la position du Soleil dans n’importe quelle vue 3D, puis la synchroniser avec l’environnement",
               (False, ())),
    ),
    (("*", "UTC Zone"),
     (("bpy.types.SunPosProperties.UTC_zone",),
      ()),
     ("fr_FR", "Fuseau horaire",
               (False, ())),
    ),
    (("*", "Difference from Greenwich, England, in hours"),
     (("bpy.types.SunPosProperties.UTC_zone",),
      ()),
     ("fr_FR", "Différence avec Greenwich, Angleterre, en heures",
               (False, ())),
    ),
    (("*", "Bind Texture to Sun"),
     (("bpy.types.SunPosProperties.bind_to_sun",
       "scripts/addons/sun_position/ui_sun.py:103"),
      ()),
     ("fr_FR", "Lier la texture au Soleil",
               (False, ())),
    ),
    (("*", "If enabled, the environment texture moves with the Sun"),
     (("bpy.types.SunPosProperties.bind_to_sun",),
      ()),
     ("fr_FR", "Si actif, la texture d’environnement tourne avec le Soleil",
               (False, ())),
    ),
    (("*", "Enter coordinates from an online map"),
     (("bpy.types.SunPosProperties.coordinates",),
      ()),
     ("fr_FR", "Saisir des coordonnées depuis une carte en ligne",
               (False, ())),
    ),
    (("*", "Day"),
     (("bpy.types.SunPosProperties.day",),
      ()),
     ("fr_FR", "Jour",
               (False, ())),
    ),
    (("*", "Day of Year"),
     (("bpy.types.SunPosProperties.day_of_year",),
      ()),
     ("fr_FR", "Jour de l’année",
               (False, ())),
    ),
    (("*", "Rotation angle of the Sun and environment texture"),
     (("bpy.types.SunPosProperties.hdr_azimuth",),
      ()),
     ("fr_FR", "Angle de rotation du Soleil et de la texture d’environnement",
               (False, ())),
    ),
    (("*", "Elevation"),
     (("bpy.types.SunPosProperties.hdr_elevation",
       "scripts/addons/sun_position/ui_sun.py:185"),
      ()),
     ("fr_FR", "Hauteur",
               (False, ())),
    ),
    (("*", "Elevation angle of the Sun"),
     (("bpy.types.SunPosProperties.hdr_elevation",
       "bpy.types.SunPosProperties.sun_elevation"),
      ()),
     ("fr_FR", "Angle de hauteur du Soleil",
               (False, ())),
    ),
    (("*", "Name of the environment texture to use. World nodes must be enabled and the color set to an environment Texture"),
     (("bpy.types.SunPosProperties.hdr_texture",),
      ()),
     ("fr_FR", "Nom de la texture d’environnement à utiliser. Les nœuds de shader du monde doivent être activés, et la couleur utiliser une texture d’environnement",
               (False, ())),
    ),
    (("*", "Latitude"),
     (("bpy.types.SunPosProperties.latitude",),
      ()),
     ("fr_FR", "Latitude",
               (False, ())),
    ),
    (("*", "Latitude: (+) Northern (-) Southern"),
     (("bpy.types.SunPosProperties.latitude",),
      ()),
     ("fr_FR", "Latitude : (+) nord (-) sud",
               (False, ())),
    ),
    (("*", "Longitude"),
     (("bpy.types.SunPosProperties.longitude",),
      ()),
     ("fr_FR", "Longitude",
               (False, ())),
    ),
    (("*", "Longitude: (-) West of Greenwich (+) East of Greenwich"),
     (("bpy.types.SunPosProperties.longitude",),
      ()),
     ("fr_FR", "Longitude : (-) ouest depuis Greenwich (+) est depuis Greenwich",
               (False, ())),
    ),
    (("*", "Month"),
     (("bpy.types.SunPosProperties.month",),
      ()),
     ("fr_FR", "Mois",
               (False, ())),
    ),
    (("*", "North Offset"),
     (("bpy.types.SunPosProperties.north_offset",
       "scripts/addons/sun_position/ui_sun.py:181"),
      ()),
     ("fr_FR", "Décalage du nord",
               (False, ())),
    ),
    (("*", "Rotate the scene to choose the North direction"),
     (("bpy.types.SunPosProperties.north_offset",),
      ()),
     ("fr_FR", "Tourner la scène pour choisir la direction du nord",
               (False, ())),
    ),
    (("*", "Collection of objects used to visualize the motion of the Sun"),
     (("bpy.types.SunPosProperties.object_collection",),
      ()),
     ("fr_FR", "Collection d’objets utilisée pour visualiser la trajectoire du Soleil",
               (False, ())),
    ),
    (("*", "Type of Sun motion to visualize."),
     (("bpy.types.SunPosProperties.object_collection_type",),
      ()),
     ("fr_FR", "Type de trajectoire du Soleil à visualiser",
               (False, ())),
    ),
    (("*", "Analemma"),
     (("bpy.types.SunPosProperties.object_collection_type:'ANALEMMA'",),
      ()),
     ("fr_FR", "Analemme",
               (False, ())),
    ),
    (("*", "Trajectory of the Sun in the sky during the year, for a given time of the day"),
     (("bpy.types.SunPosProperties.object_collection_type:'ANALEMMA'",),
      ()),
     ("fr_FR", "Trajectoire du Soleil pendant l’année, pour une heure donnée du jour",
               (False, ())),
    ),
    (("*", "Diurnal"),
     (("bpy.types.SunPosProperties.object_collection_type:'DIURNAL'",),
      ()),
     ("fr_FR", "Diurne",
               (False, ())),
    ),
    (("*", "Trajectory of the Sun in the sky during a single day"),
     (("bpy.types.SunPosProperties.object_collection_type:'DIURNAL'",),
      ()),
     ("fr_FR", "Trajectoire du Soleil pendant un seul jour",
               (False, ())),
    ),
    (("*", "Show Analemmas"),
     (("bpy.types.SunPosProperties.show_analemmas",),
      ()),
     ("fr_FR", "Afficher les analemmes",
               (False, ())),
    ),
    (("*", "Draw Sun analemmas. These help visualize the motion of the Sun in the sky during the year, for each hour of the day"),
     (("bpy.types.SunPosProperties.show_analemmas",),
      ()),
     ("fr_FR", "Afficher les analemmes du soleil. Ils aident à visualiser la trajectoire du Soleil dans le ciel pendant l’année, pour chaque heure du jour",
               (False, ())),
    ),
    (("*", "Show North"),
     (("bpy.types.SunPosProperties.show_north",),
      ()),
     ("fr_FR", "Afficher le nord",
               (False, ())),
    ),
    (("*", "Draw a line pointing to the north"),
     (("bpy.types.SunPosProperties.show_north",),
      ()),
     ("fr_FR", "Afficher une ligne pointant le nord",
               (False, ())),
    ),
    (("*", "Show Surface"),
     (("bpy.types.SunPosProperties.show_surface",),
      ()),
     ("fr_FR", "Afficher la surface",
               (False, ())),
    ),
    (("*", "Draw the surface that the Sun occupies in the sky"),
     (("bpy.types.SunPosProperties.show_surface",),
      ()),
     ("fr_FR", "Afficher la surface que le Soleil occupe dans le ciel",
               (False, ())),
    ),
    (("*", "Name of the sky texture to use"),
     (("bpy.types.SunPosProperties.sky_texture",),
      ()),
     ("fr_FR", "Nom de la texture de ciel à utiliser",
               (False, ())),
    ),
    (("*", "Sun Azimuth"),
     (("bpy.types.SunPosProperties.sun_azimuth",),
      ()),
     ("fr_FR", "Azimut du Soleil",
               (False, ())),
    ),
    (("*", "Rotation angle of the Sun from the direction of the north"),
     (("bpy.types.SunPosProperties.sun_azimuth",),
      ()),
     ("fr_FR", "Angle de rotation du Soleil depuis la direction du nord",
               (False, ())),
    ),
    (("*", "Distance to the Sun from the origin"),
     (("bpy.types.SunPosProperties.sun_distance",),
      ()),
     ("fr_FR", "Distance entre l’origine et le Soleil",
               (False, ())),
    ),
    (("*", "Sun Object"),
     (("bpy.types.SunPosProperties.sun_object",),
      ()),
     ("fr_FR", "Objet Soleil",
               (False, ())),
    ),
    (("*", "Sun object to use in the scene"),
     (("bpy.types.SunPosProperties.sun_object",),
      ()),
     ("fr_FR", "Objet Soleil à utiliser dans la scène",
               (False, ())),
    ),
    (("*", "Sunrise Time"),
     (("bpy.types.SunPosProperties.sunrise_time",),
      ()),
     ("fr_FR", "Heure de lever",
               (False, ())),
    ),
    (("*", "Time at which the Sun rises"),
     (("bpy.types.SunPosProperties.sunrise_time",),
      ()),
     ("fr_FR", "Heure à laquelle le Soleil se lève",
               (False, ())),
    ),
    (("*", "Sunset Time"),
     (("bpy.types.SunPosProperties.sunset_time",),
      ()),
     ("fr_FR", "Heure de coucher",
               (False, ())),
    ),
    (("*", "Time at which the Sun sets"),
     (("bpy.types.SunPosProperties.sunset_time",),
      ()),
     ("fr_FR", "Heure à laquelle le Soleil se couche",
               (False, ())),
    ),
    (("*", "Time of the day"),
     (("bpy.types.SunPosProperties.time",),
      ()),
     ("fr_FR", "Heure du jour",
               (False, ())),
    ),
    (("*", "Time Spread"),
     (("bpy.types.SunPosProperties.time_spread",),
      ()),
     ("fr_FR", "Plage horaire",
               (False, ())),
    ),
    (("*", "Time period around which to spread object collection"),
     (("bpy.types.SunPosProperties.time_spread",),
      ()),
     ("fr_FR", "Plage horaire à visualiser par les objets de la collection",
               (False, ())),
    ),
    (("*", "Usage Mode"),
     (("bpy.types.SunPosProperties.usage_mode",),
      ()),
     ("fr_FR", "Mode d’utilisation",
               (False, ())),
    ),
    (("*", "Operate in normal mode or environment texture mode"),
     (("bpy.types.SunPosProperties.usage_mode",),
      ()),
     ("fr_FR", "Passer en mode normal ou texture d’environnement",
               (False, ())),
    ),
    (("*", "Sun + HDR texture"),
     (("bpy.types.SunPosProperties.usage_mode:'HDR'",),
      ()),
     ("fr_FR", "Soleil et texture HDRI",
               (False, ())),
    ),
    (("*", "Use day of year"),
     (("bpy.types.SunPosProperties.use_day_of_year",),
      ()),
     ("fr_FR", "Utiliser le jour de l’année",
               (False, ())),
    ),
    (("*", "Use a single value for the day of year"),
     (("bpy.types.SunPosProperties.use_day_of_year",),
      ()),
     ("fr_FR", "Utiliser une seule valeur pour le jour de l’année",
               (False, ())),
    ),
    (("*", "Daylight savings time adds 1 hour to standard time"),
     (("bpy.types.SunPosProperties.use_daylight_savings",),
      ()),
     ("fr_FR", "L’heure d’été ajoute une heure à l’heure standard",
               (False, ())),
    ),
    (("*", "Use Refraction"),
     (("bpy.types.SunPosProperties.use_refraction",),
      ()),
     ("fr_FR", "Utiliser la réfraction",
               (False, ())),
    ),
    (("*", "Show the apparent Sun position due to atmospheric refraction"),
     (("bpy.types.SunPosProperties.use_refraction",),
      ()),
     ("fr_FR", "Afficher la position apparente du Soleil due à la réfraction atmosphérique",
               (False, ())),
    ),
    (("*", "Year"),
     (("bpy.types.SunPosProperties.year",),
      ()),
     ("fr_FR", "Année",
               (False, ())),
    ),
    (("*", "Unknown projection"),
     (("scripts/addons/sun_position/hdr.py:181",),
      ()),
     ("fr_FR", "Projection inconnue",
               (False, ())),
    ),
    (("*", "Enter/LMB: confirm, Esc/RMB: cancel, MMB: pan, mouse wheel: zoom, Ctrl + mouse wheel: set exposure"),
     (("scripts/addons/sun_position/hdr.py:252",),
      ()),
     ("fr_FR", "Entrée/ClicG : Confirmer, Échap/ClicD : Annuler, ClicM : défiler, "
               "molette : zoom, Ctrl + molette : exposition",
               (False, ())),
    ),
    (("*", "Could not find 3D View"),
     (("scripts/addons/sun_position/hdr.py:263",),
      ()),
     ("fr_FR", "Impossible de trouver la vue 3D",
               (False, ())),
    ),
    (("*", "Please select an Environment Texture node"),
     (("scripts/addons/sun_position/hdr.py:269",),
      ()),
     ("fr_FR", "Veuillez utiliser un nœud de texture d’environnement",
               (False, ())),
    ),
    (("*", "Show options and info:"),
     (("scripts/addons/sun_position/properties.py:297",),
      ()),
     ("fr_FR", "Afficher les options et infos :",
               (False, ())),
    ),
    (("*", "ERROR: Could not parse coordinates"),
     (("scripts/addons/sun_position/sun_calc.py:54",),
      ()),
     ("fr_FR", "ERREUR : Impossible d’analyser les coordonnées",
               (False, ())),
    ),
    (("Hour", "Time"),
     (("scripts/addons/sun_position/ui_sun.py:224",),
      ()),
     ("fr_FR", "Heure",
               (False, ())),
    ),
    (("*", "Time Local:"),
     (("scripts/addons/sun_position/ui_sun.py:242",),
      ()),
     ("fr_FR", "Heure locale :",
               (False, ())),
    ),
    (("*", "UTC:"),
     (("scripts/addons/sun_position/ui_sun.py:243",),
      ()),
     ("fr_FR", "UTC :",
               (False, ())),
    ),
    (("*", "Please select World in the World panel."),
     (("scripts/addons/sun_position/ui_sun.py:97",
       "scripts/addons/sun_position/ui_sun.py:140"),
      ()),
     ("fr_FR", "Veuillez sélectionner le monde dans le panneau Monde",
               (False, ())),
    ),
    (("*", "Show"),
     (("scripts/addons/sun_position/ui_sun.py:144",),
      ()),
     ("fr_FR", "Afficher",
               (False, ())),
    ),
    (("*", "North"),
     (("scripts/addons/sun_position/ui_sun.py:145",),
      ()),
     ("fr_FR", "Nord",
               (False, ())),
    ),
    (("*", "Analemmas"),
     (("scripts/addons/sun_position/ui_sun.py:146",),
      ()),
     ("fr_FR", "Analemmes",
               (False, ())),
    ),
    (("*", "Surface"),
     (("scripts/addons/sun_position/ui_sun.py:147",),
      ()),
     ("fr_FR", "Surface",
               (False, ())),
    ),
    (("*", "Use"),
     (("scripts/addons/sun_position/ui_sun.py:150",),
      ()),
     ("fr_FR", "Utiliser",
               (False, ())),
    ),
    (("*", "Azimuth"),
     (("scripts/addons/sun_position/ui_sun.py:186",),
      ()),
     ("fr_FR", "Azimut",
               (False, ())),
    ),
    (("*", "Sunrise:"),
     (("scripts/addons/sun_position/ui_sun.py:259",),
      ()),
     ("fr_FR", "Lever :",
               (False, ())),
    ),
    (("*", "Sunset:"),
     (("scripts/addons/sun_position/ui_sun.py:260",),
      ()),
     ("fr_FR", "Coucher :",
               (False, ())),
    ),
    (("*", "Please activate Use Nodes in the World panel."),
     (("scripts/addons/sun_position/ui_sun.py:94",
       "scripts/addons/sun_position/ui_sun.py:137"),
      ()),
     ("fr_FR", "Veuillez activer Utiliser nœuds dans le panneau Monde",
               (False, ())),
    ),
    (("*", "World > Sun Position"),
     (("Add-on Sun Position info: location",),
      ()),
     ("fr_FR", "Monde > Position du Soleil",
               (False, ())),
    ),
    (("*", "Show sun position with objects and/or sky texture"),
     (("Add-on Sun Position info: description",),
      ()),
     ("fr_FR", "Afficher la position du Soleil avec des objets ou une texture de ciel",
               (False, ())),
    ),
)

translations_dict = {}
for msg in translations_tuple:
    key = msg[0]
    for lang, trans, (is_fuzzy, comments) in msg[2:]:
        if trans and not is_fuzzy:
            translations_dict.setdefault(lang, {})[key] = trans

# ##### END AUTOGENERATED I18N SECTION #####
