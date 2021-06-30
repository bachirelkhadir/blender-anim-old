import os
import sys
import hashlib
from pathlib import Path
from random import randint
import bpy
from config import CONFIG
from mathutils import Vector


import src.utils as utils
sys.path.append(utils.get_current_path())

import src.tex_file_writing as tex2bpy



CURRENT_PATH = utils.get_current_path()

TEX_USE_CTEX = False
TEX_TEXT_TO_REPLACE = "YourTextHere"

# DEFAULT values
SVG_CLEANER_BIN = CONFIG.get("SVG_CLEANER_BIN", os.path.join(CURRENT_PATH, "../svgcleaner-bin/svgcleaner"))
FFMPEG_BIN = CONFIG.get("FFMPEG_BIN", "ffmpeg")
#BLENDER_BIN = "/Applications/Blender.app/Contents/MacOS/Blender" # "blender"
BLENDER_BIN = CONFIG.get("BLENDER_BIN", "blender")
XDG_OPEN = CONFIG.get("XDG_OPEN", "open") # "xdg-open"

TEX_DIR = os.path.join(CURRENT_PATH, "temps/")
ASSETS_DIR = os.path.join(CURRENT_PATH, "assets/")
OUTPUTS_DIR = os.path.join(CURRENT_PATH, "outputs/")
TEMPLATE_TEX_FILE = os.path.join(
    ASSETS_DIR,
    "tex_template.tex"
)

EXTRA_PATHS = CONFIG.get("EXTRA_PATHS", [""])

RIGHT = Vector([1, 0, 0])
UP = Vector([0, 1, 0])
OUT = Vector([0, 0, 1])
LEFT = -RIGHT
DOWN = -UP
IN = -OUT



#FPS_QUALITY = {'LOW': 15, 'MEDIUM': 30, 'HIGH': 60, 'VERY_HIGH': 60}

#RESOLUTION_QUALITY = {'LOW': (1920//4, 1080//4), 'MEDIUM': (1920//2, 1080//2), 'HIGH': (1920, 1080),
#                      'VERY_HIGH': (1920*2, 1080*2)}

ENGINE =  CONFIG.get("ENGINE", 'BLENDER_EEVEE') # 'CYCLES'
FPS = CONFIG.get("FPS", 60)

#ENGINE =  "CYCLES"

for path_dir in (ASSETS_DIR, TEX_DIR, OUTPUTS_DIR):
    utils.create_folder_if_needed(path_dir)
