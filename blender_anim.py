import numpy as np
import os
import sys
import hashlib
from pathlib import Path
from random import randint
import bpy
import logging
from src.consts import *

# hack to set logging to debug level if the line "DEBUG = True" is present

logging.basicConfig(level=LOGGING_LEVEL,
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


def save_and_render(class_scene, start=None, end=None, **scene_kwargs):
    scene = class_scene(**scene_kwargs)
    scene.construct()
    class_name = class_scene.__name__

    destination = f"outputs/{class_name}/"
    destination_render = os.path.join(destination,
                                      "images",
                                      class_name,
                                      )



    if start is None:
        start = 1
    if  end is None:
        end = scene.last_frame+1

    bpy.data.scenes["Scene"].render.filepath = destination_render
    bpy.data.scenes["Scene"].frame_end = end

    log.info(f"Saving render blend file to {destination}")
    utils.create_folder_if_needed(destination)
    save_blend_file(os.path.join(destination, f"{class_name}.blend"))
    scene.print_animation_outline()

    # XXXXX
    return
    log.info(f"Start @ frame {start} and end @ {end}")

    if cmd_args.render_pngs:
        logging.info("-"*50)
        logging.info("Rendering")
        scene.render(start, end, filename=destination_render)



def RADIANS(deg):
    return deg * np.pi/180.
