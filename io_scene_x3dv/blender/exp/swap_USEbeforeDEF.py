from x3d import *
import copy

USEdict = {}
DEFdict = {}
USEbeforeDEFdict = {}

def swap_USEbeforeDEF(node=None, parent=None):
    USE = getattr(node,'USE', None)
    if USE:
        if USE not in USEdict:
            USEdict[USE] = [{'node': node, 'parent': parent}]
        else:
            USEdict[USE].append({'node': node, 'parent': parent})
        print(node.NAME(), 'USE: ' + USE + str(len(USEdict[USE])))
        if USE not in DEFdict:
            print ("USE " + USE + " occurred before DEF")
            USEbeforeDEFdict[USE] = USEdict[USE] # record in dict
    DEF = getattr(node,'DEF', None)
    if DEF:
        if DEF not in DEFdict: DEFdict[DEF] = [node]
        else:
            DEFdict[DEF].append(node)
            print ("DEF " + DEF + " already defined")
            if DEF not in USEbeforeDEFdict:
                print ("creating a new USE node of the same type")
                insertDEFIndex = parent.children.index(node)
                nodeClass = node.NAME()
                node = globals()[nodeClass](USE=DEF) # a bit hackish
                parent.children[insertDEFIndex] = node
                # use node.FIELD_DECLARATIONS to reset all fields to defaults in case of deepcopy approach
        print(node.NAME(),'DEF: ' + DEF + str(len(DEFdict[DEF])))
        if DEF in USEbeforeDEFdict:
            USEnode = USEbeforeDEFdict[DEF][0] # replace first USE node only
            #USEcopy = copy.deepcopy(USEnode['node'])
            if len(DEFdict[DEF]) == 1: # only for first DEF node
                print("replacing earlier USE with this DEF")
                insertUSEIndex = USEnode['parent'].children.index(USEnode['node'])
                USEnode['parent'].children[insertUSEIndex] = node
            # DEF to USE
            print("replacing DEF with copy of earlier USE")
            insertDEFIndex = parent.children.index(node)
            parent.children[insertDEFIndex] = USEnode['node'] # USEcopy
    if hasattr(node, 'children'):
        for each in node.children:
            swap_USEbeforeDEF(node=each, parent=node)
    if hasattr(node, 'skeleton'):
        for each in node.skeleton:
            swap_USEbeforeDEF(node=each, parent=node)
    if hasattr(node, 'joints'):
        for each in node.joints:
            swap_USEbeforeDEF(node=each, parent=node)
    if hasattr(node, 'sites'):
        for each in node.sites:
            swap_USEbeforeDEF(node=each, parent=node)
    if hasattr(node, 'segments'):
        for each in node.segments:
            swap_USEbeforeDEF(node=each, parent=node)
    if hasattr(node, 'skin'):
        for each in node.skin:
            swap_USEbeforeDEF(node=each, parent=node)
    if hasattr(node, 'skinCoord'):
        swap_USEbeforeDEF(node=node.skinCoord, parent=node)
    if hasattr(node, 'skinNormal'):
        swap_USEbeforeDEF(node=node.skinNormal, parent=node)
    if hasattr(node, 'motions'):
        for each in node.motions:
            swap_USEbeforeDEF(node=each, parent=node)
