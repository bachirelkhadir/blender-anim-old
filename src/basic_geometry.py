from mathutils import Vector
import bpy
import bmesh


def make_cube(loc, scale, name="Cube"):
    # Create an empty mesh and the object.
    mesh = bpy.data.meshes.new(name)
    basic_cube = bpy.data.objects.new(name, mesh)

    # Construct the bmesh cube and assign it to the blender mesh.
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bm.to_mesh(mesh)
    bm.free()

    basic_cube.location = loc
    basic_cube.scale = scale

    return basic_cube


def make_sphere(center=Vector([0,0,0]), radius=1.):
    pass
