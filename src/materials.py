from mathutils import Vector
import bpy


def color_bpy_object(ob, color_rgba):
    mat = bpy.data.materials.new(f"{ob.name} Material")
    mat.use_nodes = True
    mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = color_rgba
    ob.data.materials.append(mat)
    return mat
