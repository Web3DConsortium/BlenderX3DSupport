import bpy

def getscenescale(scene):
    unit_settings = scene.unit_settings

    if unit_settings.system in {"METRIC", "IMPERIAL"}:
        length_unit = unit_settings.length_unit 
        if length_unit == 'CENTIMETERS':
            # print("Converting centimeters to meters")
            return 0.01
        else:
            print(f"Using normal metric or imperial scale {unit_settings.scale_length}")
            # this appears to be wrong for centimeters
            return unit_settings.scale_length
    else:
        # No unit system in use
        print(f"Using normal scale {unit_settings.system} {unit_settings.scale_length}")
        return 1
