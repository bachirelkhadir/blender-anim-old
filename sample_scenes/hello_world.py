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
line = scene.add_line(start=(-3, -2, 0), end=(3, -2, 0), thinkness=.02)
color_bpy_object(line, (1, 0, 1, 1.))

render_info_msg = (r"Engine:" f"{scene.engine}" r"- \\"
                   "Resolution: "
                   f"{scene.resolution}")

render_info_msg = scene.add_text(render_info_msg.replace("_", " "))
render_info_msg.location = (3, 5, 0)


################
# Animations
###############

scene.play(Appear(render_info_msg))
scene.play(Appear(line))
scene.play(GraduallyAppear(line, 'x'), duration=1)

# monkey gradually disappears
scene.play(Appear(monkey))
scene.play(GraduallyAppear(monkey, 'x'), duration=1)
scene.wait(1)

if False:
    # monkey gradually appears
    scene.play(GraduallyDisappear(monkey, 'y'))
    scene.wait(1)

    # monkey rotate and sphere appears

    scene.play(Appear(monkey_copy))
    scene.wait(.5)

    # sphere transforms into monkey
    scene.play(WrapInto(monkey_copy, sphere), duration=2)
    scene.wait(2)

    # Torus enters
    scene.play(Appear(torus))
    scene.play(Translate(torus, (-2, 0, 0)))
    scene.wait(1)
    scene.play(Rotate(torus, (3, 2, 1)), duration=2)
    scene.wait(2)
    scene.play(WrapInto(torus, monkey), duration=2)
    scene.wait(2)




# scene.play(Rotate(torus, (3, 2, 1)), duration=5)
# scene.wait(1)
# scene.play(Appear(render_info_msg))
# scene.play(Translate(render_info_msg, (0, -2, 0)), duration=1)
# scene.wait(3)

# scene.play(Appear(monkey))

# scene.wait(2)
# scene.play(Appear(monkey))
# scene.play(Translate(monkey, (0, 5, 0)), duration=2)
# scene.wait(1)
# scene.play(Translate(monkey, (5, 0, 0)), duration=2)



log.info("Saving render blend file")
save_blend_file("outputs/render.blend")

start, end = map(int, cmd_args.start_end_frame.split(','))
log.info("Start @ frame {start} and end @ {end}")

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
# compile-command: "cd .. && blender --background assets/monkey_sphere.blend --python sample_scenes/hello_world.py -- -lrvp"
# End:
