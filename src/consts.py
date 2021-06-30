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
ZERO = 0*UP
ONE = Vector([1, 1, 1])



ENGINE =  CONFIG.get("ENGINE", 'BLENDER_EEVEE') # 'CYCLES'
#ENGINE =  "CYCLES"
FPS = CONFIG.get("FPS", 60)
RESOLUTION = CONFIG.get("RESOLUTION", (1920, 1080))
LOGGING_LEVEL = logging.info

for path_dir in (ASSETS_DIR, TEX_DIR, OUTPUTS_DIR):
    utils.create_folder_if_needed(path_dir)
