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

from src.consts import *
from src.utils import *
from src.animations import *
from src.scene import *
from src.materials import *

# End Imports


scene = Scene(fps=15)

sphere = bpy.data.objects["Sphere"]
monkey = bpy.data.objects["Monkey"]
#monkey2 = deep_copy_object(monkey)
torus = bpy.data.objects["Torus"]
cube = scene.add_cube(loc=(-5, 5, 0), scale=(3,3,3))
color_bpy_object(cube, (.5, .1, 0.25, 1.))

text = scene.add_text(r"Sample Scene")
text.location = (3, 0, 1)


render_info_msg = (f"Engine: {bpy.context.scene.render.engine} - "
                   f"{consts.RESOLUTION}")
render_info_msg = scene.add_text(render_info_msg.replace("_", " "))
render_info_msg.scale *= .5
render_info_msg.location = (-3, -5, 0)


scene.play(Rotate(cube, [0, .8*np.pi, -2*np.pi]), duration=2)
scene.play(WrapInto(sphere, monkey))
scene.play(Rotate(torus, [0, 0, np.pi]), duration=2)
scene.wait(1)
scene.play(Translate(cube, [10, 0, 0]), duration=2)
# scene.play(Disappear(monkey))




log.info("Saving render blend file")
save_blend_file("outputs/render.blend")



logging.info("Rendering")

bpy.context.scene.render.resolution_x = RESOLUTION[0]
bpy.context.scene.render.resolution_y = RESOLUTION[1]

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
