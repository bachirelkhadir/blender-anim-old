from mathutils import Vector
import bpy
import bmesh
import math


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


def make_line(start, end, thinkness, name="Line"):
    dx, dy, dz = diff = end-start
    dist = diff.length
    center = (start + end)/2
    # TODO: avoid ops so that the objects doesn't get added to the selected
    # collection
    bpy.ops.mesh.primitive_cylinder_add(
        radius=thinkness,
        depth=dist,
        location=center
    )
    cylinder = bpy.context.object
    phi = math.atan2(dy, dx)
    theta = math.acos(dz/dist)

    cylinder.rotation_euler[1] = theta
    cylinder.rotation_euler[2] = phi
    return cylinder


def make_sphere(center=Vector([0,0,0]), radius=1.):
    pass
