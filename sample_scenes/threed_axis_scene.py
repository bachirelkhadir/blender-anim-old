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
                    format="%(levelname)-5s: %(name)-9s | %(asctime)-15s | %(message)s")
log = logging.getLogger(__name__)
sys.path.append(os.path.dirname(os.path.dirname(bpy.data.filepath)))
sys.path.append('/home/bachir/.local/lib/python3.7/site-packages')


from tqdm import tqdm, trange

from src.consts import *
from src.utils import *
from src.animations import Appear, Rotate, Scale
from src.scene import *
from src.materials import *
from src.vobject import VGroup
# End Imports


cmd_args = parse_cmd_arguments()
log.info(cmd_args)

quality = 'MEDIUM'
if cmd_args.high_quality:
    quality = 'HIGH'
if cmd_args.low_quality:
    quality = 'LOW'

#############################

scene = Scene(quality=quality)

################
# Scene Objects
###############

# preexisting objects
sphere = bpy.data.objects["Sphere"]
monkey = bpy.data.objects["Monkey"]
torus = bpy.data.objects["Torus"]

# programmatically created objects
# Monkey
monkey_copy = scene.duplicate_object(monkey)
monkey_copy.location[1] -= 3

# Cube
cube = scene.add_cube(loc=(-5, 5, 0), scale=(3,3,3))
color_bpy_object(cube, (.5, .1, 0.25, 1.))

# line
axis = scene.add_3d_axis(thickness=.02)
for line in axis:
    color_bpy_object(line, (1, 0, 1, 1.))

render_info_msg = (r"Engine:" f"{scene.engine}" r"- \\"
                   "Resolution: "
                   f"{scene.resolution}")

render_info_msg = scene.add_text(render_info_msg.replace("_", " "))
render_info_msg.location = (3, 5, 0)


################
# Animations
###############

# scene.play(Appear(monkey))
scene.play(Rotate(monkey, (3, 2, 1)), duration=1)
for line in axis:
    scene.play(Appear(line))
scene.play(Scale(VGroup(*axis), (5, 5, 5)), duration=0)
scene.play(Rotate(VGroup(*axis), (0, 1, 1)), duration=1)

# monkey gradually disappears
scene.wait(1)

log.info("Saving render blend file")
save_blend_file("outputs/render.blend")

start, end = map(int, cmd_args.start_end_frame.split(','))
log.info(f"Start @ frame {start} and end @ {end}")

if cmd_args.render_pngs:
    logging.info("Rendering")
    scene.render(start, end)

if cmd_args.make_video:
    logging.info("Making video")
    scene.write_frames_to_video(start, end)

if cmd_args.play_video:
    logging.info("Opening video")
    scene.open_video()

elif cmd_args.open_blender:
    logging.info("Opening blender file")
    scene.open_blender()



# Local Variables:
# compile-command: "cd .. && blender --background assets/monkey_sphere.blend --python sample_scenes/threed_axis_scene.py -- -lrvp"
# End:
