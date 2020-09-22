import os
import sys
import hashlib
from pathlib import Path
from random import randint

#sys.path.append("src")

from . tex_file_writing import *


USE_BLENDER = True
try:
    import bpy
except ImportError:
    USE_BLENDER = True


def get_current_path():
    file_path = os.path.realpath(__file__)    
    if USE_BLENDER:
        file_path = bpy.data.filepath
    return os.path.dirname(file_path)


TEX_USE_CTEX = False
TEX_TEXT_TO_REPLACE = "YourTextHere"
TEX_DIR = "temps"
CURRENT_PATH = get_current_path()
TEMPLATE_TEX_FILE = os.path.join(
    CURRENT_PATH,
    "assets/tex_template.tex"
)


print(f"Use blender? {USE_BLENDER}")
print(f"Current path: {CURRENT_PATH}")




ob = bpy.data.objects["Sphere"]
frame_number = 0

for i in range(50):
    x, y, z = [randint(-20, 20) for _ in range(3)]
    bpy.context.scene.frame_set(frame_number)
    ob.location = (x, y, z)
    ob.keyframe_insert(data_path="location", index=-1)
    frame_number += 5
    
