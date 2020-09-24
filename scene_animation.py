# Imports
import numpy as np
import os
import sys
import hashlib
from pathlib import Path
from random import randint
import bpy
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)-5s: %(name)-9s |  %(asctime)-15s | %(message)s")
log = logging.getLogger(__name__)
sys.path.append(os.path.dirname(os.path.dirname(bpy.data.filepath)))
sys.path.append('/home/bachir/.local/lib/python3.7/site-packages')


from tqdm import tqdm, trange

import src.consts as consts
import src.utils as utils
import src.animations as animations
import src.scene as scene
import src.materials as materials
# End Imports


hellow_world_scene = scene.Scene(fps=15)

sphere = bpy.data.objects["Sphere"]
monkey = bpy.data.objects["Monkey"]
monkey2 = utils.deep_copy_object(monkey)

torus = bpy.data.objects["Torus"]


text = hellow_world_scene.add_text(r"\textcolor{black}{T}\textcolor{red}{e}xt!!")
text.location[0] += 3
text.location[1] = 0


render_info_msg = (f"Engine: {bpy.context.scene.render.engine} - "
                   f"{consts.RESOLUTION}")
render_info_msg = hellow_world_scene.add_text(render_info_msg.replace("_", " "))
render_info_msg.scale *= .5
render_info_msg.location[0] -= 3
render_info_msg.location[1] -= 5

timeline = hellow_world_scene.timeline

# Text => Monkey
#timeline.play_animation(animations.WrapInto(text.children[0], monkey), duration=1)

cube = hellow_world_scene.add_cube()
materials.color_bpy_object(cube, (.5, .1, 0.25, 1.))
cube.location[1] += 3
cube.scale *= 3


cube2 = hellow_world_scene.add_cube()
materials.color_bpy_object(cube2, (1., .1, 0.25, 1.))
cube2.location[1] -= 3
cube2.scale *= 3

hellow_world_scene.play(animations.Rotate(cube2, [0, .8*np.pi, -2*np.pi]), duration=2)
hellow_world_scene.play(animations.Translate(cube2, [.2, 1, 0]), duration=2)


hellow_world_scene.play(animations.Disappear(monkey))
hellow_world_scene.play(animations.Rotate(torus, [0, 0, np.pi]), duration=2)
hellow_world_scene.wait(.5)
hellow_world_scene.play(animations.Appear(monkey))
hellow_world_scene.play(animations.Rotate(cube, [0, 0, 2*np.pi]), duration=10)



# # monkey => sphere
# timeline.play_animation(animations.WrapInto(monkey, sphere), duration=1)
# timeline.wait(1)
# # sphere => monkey
# monkey2.animation_data_clear()
# timeline.play_animation(animations.WrapInto(sphere, monkey2), duration=1)
# # hide monkey
# timeline.play_animation(animations.Disappear(monkey, 'y'), duration=1)



log.info("Saving render blend file")
utils.save_blend_file("outputs/render.blend")



logging.info("Rendering")

bpy.context.scene.render.resolution_x = consts.RESOLUTION[0]
bpy.context.scene.render.resolution_y = consts.RESOLUTION[1]







# redirect output to log file
logfile = 'blender_render.log'
open(logfile, 'a').close()
old = os.dup(1)
sys.stdout.flush()
os.close(1)
os.open(logfile, os.O_WRONLY)


idx = 0
for frame_number in trange(0, 30, 1, desc="Rendering frame"):
    log.debug(f"Rendering frame {frame_number}")
    log.debug(f"Image size ({bpy.context.scene.render.resolution_x}, {bpy.context.scene.render.resolution_y})" )
    bpy.context.scene.render.filepath = os.path.join(
        consts.CURRENT_PATH,
        f"outputs/render-frame{frame_number:02}.png"
    )
    bpy.context.scene.frame_set(frame_number)
    bpy.ops.render.render(write_still=True)
    idx += 1
# disable output redirection
os.close(1)
os.dup(old)
os.close(old)


# to view render:
#  eog outputs/render.png 

# Local Variables:
# compile-command: "blender --background assets/monkey_sphere.blend --python scene_animation.py"
# End:
