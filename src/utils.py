import logging
import os
import sys
from pathlib import Path
import bpy
import bmesh
from mathutils import Vector, Matrix
import src.consts as consts
import argparse
import subprocess as sp


def get_blend_path():
    file_path = bpy.data.filepath
    return os.path.dirname(os.path.dirname(file_path))

def get_current_path():
    """Path of the blender-anim library"""
    return Path(__file__).absolute().parent.parent

def create_folder_if_needed(path):
    if not os.path.exists(path):
        os.makedirs(path)

def parse_cmd_arguments():
    argv = sys.argv

    if '--' not in argv:
        argv = []
    else:
        argv = argv[argv.index("--") + 1:]  # get all args after "--"

    parser = argparse.ArgumentParser(description='blender-anim')

    parser.add_argument('-H', help="High quality", action="store_true", dest="high_quality", default=False)
    parser.add_argument('-l', help="Low quality", action="store_true", dest="low_quality", default=False)
    parser.add_argument('-p', help="Play video at the end", action="store_true", dest="play_video", default=False)
    parser.add_argument('-b', help="Open blender file", action="store_true", dest="open_blender", default=False)
    parser.add_argument('-r', help="Render pngs", action="store_true", dest="render_pngs", default=False)
    parser.add_argument('-v', help="Write png frames to video with ffmpeg", action="store_true", dest="make_video", default=False)

    parser.add_argument('-n', help="Start/End frame", type=str, dest="start_end_frame", default='-1,-1')


    return parser.parse_args(argv)

def exec_silently(commands):
    FNULL = open(os.devnull, 'w')
    sp.call(commands, stdout=FNULL, stderr=sp.STDOUT)
    FNULL.close()


def get_aligned_bounding_box(ob):
    ob = deep_copy_object(ob)
    bbox_corners = [tuple(ob.matrix_world @ Vector(corner)) for corner in ob.bound_box]
    lower_vert = Vector([ min([v[i] for v in bbox_corners]) for i in range(3) ])
    upper_vert = Vector([ max([v[i] for v in bbox_corners]) for i in range(3) ])
    center = (upper_vert + lower_vert)/2
    scale = upper_vert - lower_vert

    # center = ob.matrix_world @ ob.location
    # scale = ob.matrix_world @ ob.dimensions
    # avoid 2D box
    scale += Vector([1, 1, 1]) * 1e-3
    return (center, scale)





def deep_copy_object(obj):
    copy = obj.copy()
    copy.data = obj.data.copy()
    copy.animation_data_clear()
    # if copy.data.shape_keys:
    #     copy.data.shape_keys.animation_data_clear()
    # copy.modifiers.clear()
    copy.active_material = obj.active_material.copy()
    return copy


# https://sinestesia.co/blog/tutorials/python-rounded-cube/
def apply_modifiers(obj):
    """ Apply all modifiers on an object """

    bm = bmesh.new()
    dg = bpy.context.evaluated_depsgraph_get()
    bm.from_object(obj, dg)
    bm.to_mesh(obj.data)
    bm.free()
    obj.modifiers.clear()


def select_obj(obj):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def import_svg_in_blender_as_collection(svg_filepath):
    # trick to find the objects created for the import:
    collections_pre_import = set([ o.name for o in bpy.data.collections ])
    bpy.ops.import_curve.svg(filepath=svg_filepath)
    collections_post_import = set([ o.name for o in bpy.data.collections ])
    new_collection = collections_post_import.difference(collections_pre_import).pop()
    return new_collection


def create_bpy_collection(name="New Collection", hide_viewport=False, hide_render=False):
        scene_master_col = bpy.context.scene.collection
        new_col = bpy.data.collections.new(name)
        scene_master_col.children.link(new_col)
        new_col.hide_viewport = hide_viewport
        new_col.hide_render = hide_render
        return new_col


def remove_bpy_collection(col):
    scene_master_col = bpy.context.scene.collection
    scene_master_col.children.unlink(col)


def save_blend_file(path):

    logging.info(f"Saving blend file to {path}")
    bpy.ops.wm.save_as_mainfile(filepath=path)
    # bpy.ops.wm.save_as_mainfile(filepath=os.path.join(
    #     consts.CURRENT_PATH,
    #     path
    # ))



def bpy_apply_transform(ob, location=True, rotation=True, scale=True):
    bpy.ops.object.select_all(action='DESELECT')
    ob.select_set(True)
    bpy.ops.object.transform_apply(location=location, rotation=rotation, scale=scale)
    return

    # Below is a low level solution but is is broken
    # as it doesn't handle rotations well

    # transform the mesh using the matrix world
    ob.data.transform(ob.matrix_world)
    # then reset matrix to identity
    ob.matrix_world = Matrix()


def bpy_halign(objs):
    bpy.ops.object.select_all(action='DESELECT')
    for ob in objs:
        ob.select_set(True)
    bpy.ops.object.align(align_axis={"X", "Y", "Z"}, align_mode="OPT_1")
    bpy.ops.object.select_all(action='DESELECT')
