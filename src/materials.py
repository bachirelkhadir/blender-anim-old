import logging
from mathutils import Vector
import bpy

def hex_to_rgba(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16)/256. for i in (0, 2, 4)) + (1,)

def color_bpy_object(ob, color_rgba):
    if type(color_rgba) == str:
        color_rgba = hex_to_rgba(color_rgba)
    if len(ob.data.materials) > 0:
        mat_name, mat = ob.data.materials.items()[0]
        logging.info(f"Applying color to object {ob.name} that already has material {mat_name}.")
    else:
        mat = bpy.data.materials.new(f"{ob.name} Material")
    mat.use_nodes = True
    mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = color_rgba
    mat.diffuse_color = color_rgba # for viewport display
    ob.data.materials.append(mat)
    return mat
