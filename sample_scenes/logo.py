#!/usr/bin/env python3

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

render_info_msg = (r"Visually Explained")

render_info_msg = scene.add_text(render_info_msg.replace("_", " "))
render_info_msg.location = (3, 5, 0)
scene.play(Appear(render_info_msg))
save_blend_file("outputs/logo.blend")
