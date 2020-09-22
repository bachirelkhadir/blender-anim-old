import os
import sys
import hashlib
from pathlib import Path
from random import randint
import bpy


def get_current_path():
    file_path = bpy.data.filepath
    return os.path.dirname(os.path.dirname(file_path))

sys.path.append(get_current_path())

import src.tex_file_writing as tex2bpy



TEX_USE_CTEX = False
TEX_TEXT_TO_REPLACE = "YourTextHere"
TEX_DIR = "temps/"
CURRENT_PATH = get_current_path()
TEMPLATE_TEX_FILE = os.path.join(
    CURRENT_PATH,
    "assets/tex_template.tex"
)
