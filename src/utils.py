import os
import bpy
import bmesh
from mathutils import Vector


def get_current_path():
    file_path = bpy.data.filepath
    return os.path.dirname(os.path.dirname(file_path))


def create_folder_if_needed(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_aligned_bounding_box(ob):
    bbox_corners = [tuple(ob.matrix_world @ Vector(corner)) for corner in ob.bound_box]
    lower_vert = Vector([ min([v[i] for v in bbox_corners]) for i in range(3) ])
    upper_vert = Vector([ max([v[i] for v in bbox_corners]) for i in range(3) ])
    center = (upper_vert + lower_vert)/2
    scale = upper_vert - lower_vert
    return (center, scale)


def make_cube(loc, scale):
    # Create an empty mesh and the object.
    mesh = bpy.data.meshes.new('Cube')
    basic_cube = bpy.data.objects.new("Cube", mesh)

    # Construct the bmesh cube and assign it to the blender mesh.
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bm.to_mesh(mesh)
    bm.free()

    basic_cube.location = loc
    basic_cube.scale = scale

    return basic_cube



# https://sinestesia.co/blog/tutorials/python-rounded-cube/
def apply_modifiers(obj):
    """ Apply all modifiers on an object """

    bm = bmesh.new()
    dg = bpy.context.evaluated_depsgraph_get()
    bm.from_object(obj, dg)
    bm.to_mesh(obj.data)
    bm.free()
    obj.modifiers.clear()
