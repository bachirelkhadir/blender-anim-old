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


cmd_args = utils.parse_cmd_arguments()
log.info(cmd_args)

quality = 'MEDIUM'
if cmd_args.high_quality:
    quality = 'HIGH'
if cmd_args.low_quality:
    quality = 'LOW'

scene = Scene(quality=quality)

# preexisting objects
sphere = bpy.data.objects["Sphere"]
monkey = bpy.data.objects["Monkey"]
torus = bpy.data.objects["Torus"]

# programmatically created objects
monkey_copy = scene.duplicate_object(monkey)

monkey_copy.location[1] -= 2
cube = scene.add_cube(loc=(-5, 5, 0), scale=(3,3,3))
color_bpy_object(cube, (.5, .1, 0.25, 1.))


render_info_msg = (r"Engine:" f"{scene.engine}" r"- \\ Resolution:"
                   f"{scene.resolution}" "\\\\"
                   r"\Huge $f(x) = \sin(x)$")

render_info_msg = scene.add_text(render_info_msg.replace("_", " "))
render_info_msg.location = (3, 5, 0)

for ob in (sphere, monkey, monkey_copy, torus, cube, render_info_msg):
    scene.play(Appear(ob))

scene.play(Rotate(monkey, [0, 2*np.pi, 0]), duration=2)
#scene.wait(1)
#scene.play(WrapInto(monkey, torus), duration=2)
#scene.wait(2)




# scene.play(Rotate(torus, (3, 2, 1)), duration=5)
# scene.wait(1)
# scene.play(Appear(render_info_msg))
# scene.play(Translate(render_info_msg, (0, -2, 0)), duration=1)
# scene.wait(3)

# scene.play(Appear(monkey))
# scene.play(WrapInto(sphere, monkey), duration=2)
# scene.wait(2)
# scene.play(Appear(monkey))
# scene.play(Translate(monkey, (0, 5, 0)), duration=2)
# scene.wait(1)
# scene.play(Translate(monkey, (5, 0, 0)), duration=2)



log.info("Saving render blend file")
save_blend_file("outputs/render.blend")

if cmd_args.render_pngs:
    logging.info("Rendering")
    scene.render()

if cmd_args.make_video:
    logging.info("Making video")
    scene.write_frames_to_video()

if cmd_args.play_video:
    logging.info("Opening video")
    scene.open_video()
elif cmd_args.open_blender:
    logging.info("Opening blender file")
    scene.open_blender()



# to view render:
#  eog outputs/render.png 

# Local Variables:
# compile-command: "cd .. && blender --background assets/monkey_sphere.blend --python sample_scenes/hello_world.py -- -lrvp"
# End:
