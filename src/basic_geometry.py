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
    # mutlitply by [1, 1, 1] in case scale is a float
    basic_cube.scale = scale * Vector([1, 1, 1])

    return basic_cube

def make_plane(loc, scale, name="Plane"):
    plane = make_cube(loc, scale, name)
    plane.scale[2] = .01

    return plane

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


def make_z_function_surface(exp_f="x**2 + y**2", name="Surf"):
    bpy.ops.mesh.primitive_z_function_surface(
                        equation=exp_f,
                        div_x=16,
                        div_y=16,
                        size_x=2,
                        size_y=2)
    surf = bpy.context.object
    return surf
