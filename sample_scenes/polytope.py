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
extra_path = os.path.dirname(os.path.dirname(bpy.data.filepath))
log.info(f"Path: {extra_path} added to path")
sys.path.append(extra_path)


from tqdm import tqdm, trange

from src.consts import *
from src.utils import *
from src.animations import *
from src.scene import *
from src.materials import *

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
# sphere = bpy.data.objects["Sphere"]
# monkey = bpy.data.objects["Monkey"]
# torus = bpy.data.objects["Torus"]

# programmatically created objects
# Monkey
# monkey_copy = scene.duplicate_object(monkey)
# monkey_copy.location[1] -= 3

# Cube
cube = scene.add_cube(loc=(2, 2, 0), scale=(1,1,1,))
color_bpy_object(cube, (0., .1, 0.25, 1.))
scene.play(Appear(cube))

plane = scene.add_plane(scale=(3, 3, 3))
plane.rotation_euler[0] = 20
plane.rotation_euler[1] = 30
color_bpy_object(plane, (1., .1, 0.25, 1.), )
scene.play(Appear(plane))

# line
line = scene.add_line(start=(-3, -2, 0), end=(3, -2, 0), thickness=.02)
color_bpy_object(line, (1, 0, 1, 1.))
scene.play(Appear(line))

render_info_msg = (r"Engine:" f"{scene.engine}" r"- \\"
                   "Resolution: "
                   f"{scene.resolution}")

#render_info_msg = scene.add_text(render_info_msg.replace("_", " "))
#render_info_msg.location = (3, 5, 0)
#scene.play(Appear(render_info_msg))


log.info("Saving render blend file")
save_blend_file("outputs/polytope.blend")

scene.render(0, 1)
