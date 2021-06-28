import sys
import os
sys.path.append(os.getcwd())

from blender_anim import *
import mathutils


scene = make_scene()


def add_text(s):
    lab = scene.add_text(s)
    lab.rotation_euler =  bpy.data.objects["Camera"].rotation_euler
    lab.scale = (.5, .5, .5)
    lab.location[0] = 3
    utils.bpy_apply_transform(lab, location=False, rotation=False, scale=True)
    color_bpy_object(lab, WHITE)
    return lab


lab = add_text("f(x) = 0")
scene.print_scene_outline()
scene.play(Appear(lab))
scene.play(Translate(lab, UP))
scene.wait()
save_and_render(scene)
