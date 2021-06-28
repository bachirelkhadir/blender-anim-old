import numpy as np
import os
import sys
import hashlib
from pathlib import Path
from random import randint
import bpy
import logging
from src.consts import *

logging.basicConfig(level=logging.ERROR,
                    format="%(levelname)-5s: %(name)-9s | %(asctime)-15s | %(message)s")
log = logging.getLogger(__name__)
log.info(f"Paths: {EXTRA_PATHS} added to path")
sys.path.extend(EXTRA_PATHS)


from tqdm import tqdm, trange
from src.consts import *
from src.utils import *
from src.animations import *
from src.scene import *
from src.materials import *
from src.color_list import *

# End Imports


cmd_args = parse_cmd_arguments()
log.info(cmd_args)

quality = 'MEDIUM'
if cmd_args.high_quality:
    quality = 'HIGH'
if cmd_args.low_quality:
    quality = 'LOW'


def make_scene():
    return Scene(quality=quality)


def save_and_render(scene):

    log.info("Saving render blend file")
    save_blend_file("outputs/render.blend")

    start, end = map(int, cmd_args.start_end_frame.split(','))
    log.info(f"Start @ frame {start} and end @ {end}")

    if cmd_args.render_pngs:
        logging.info("-"*50)
        logging.info("Rendering")
        scene.render(start, end)


    elif cmd_args.open_blender:
        logging.info("-"*50)
        logging.info("Opening blender file")
        scene.open_blender()

    sys.exit()


def RADIANS(deg):
    return deg * np.pi/180.
