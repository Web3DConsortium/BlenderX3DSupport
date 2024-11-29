import bpy
import sys
import os

from .GetSceneScale import getscenescale

x3dv_round_precision = 5
x3dv_lengthUnitConversion = getscenescale(bpy.context.scene)
def round_array(it):
    #print(f"unounded {it[:]}")
    rounded = [round(v*x3dv_lengthUnitConversion, x3dv_round_precision) for v in it]
    #print(f"rounded {rounded[:]}")
    return rounded

def round_array_no_unit_scale(it):
    #print(f"unounded {it[:]}")
    rounded = [round(v, x3dv_round_precision) for v in it]
    #print(f"rounded {rounded[:]}")
    return rounded

