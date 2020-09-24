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


scene = Scene(quality='LOW')

sphere = bpy.data.objects["Sphere"]
monkey = bpy.data.objects["Monkey"]
torus = bpy.data.objects["Torus"]
cube = scene.add_cube(loc=(-5, 5, 0), scale=(3,3,3))
color_bpy_object(cube, (.5, .1, 0.25, 1.))

render_info_msg = (r"\textcolor{blue}{Engine:}" "{scene.engine} - "
                   r"\textcolor{red}{Resolution:}" f"{scene.resolution}")
render_info_msg = scene.add_text(render_info_msg.replace("_", " "))
render_info_msg.location = (-3, 5, 0)
render_info_msg.scale *= 2

scene.play(Appear(torus))
scene.wait(2)
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

logging.info("Rendering")
scene.render()

logging.info("Making video")
scene.write_frames_to_video()

logging.info("Opening video")
scene.open_video()


# to view render:
#  eog outputs/render.png 

# Local Variables:
# compile-command: "cd .. && blender --background assets/monkey_sphere.blend --python sample_scenes/hello_world.py"
# End:
