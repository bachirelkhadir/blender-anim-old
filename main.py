import os
import sys
import hashlib
from pathlib import Path
from random import randint
import bpy
import logging


logging.basicConfig(level=logging.DEBUG,
                    format="%(levelname)-5s: %(name)-9s |  %(asctime)-15s | %(message)s")
log = logging.getLogger(__name__)

sys.path.append(os.path.dirname(os.path.dirname(bpy.data.filepath)))

import src.tex_file_writing as tex2bpy
import src.consts as consts
import src.utils as utils




ob = bpy.data.objects["Sphere"]
frame_number = 0


svg_obj = tex2bpy.tex_to_bpy(r"hello world! $x=1$")
svg_obj.location[0] -= 3

svg_obj = tex2bpy.tex_to_bpy(r"abcdef \textcolor{red}{12345} \Huge \textcolor{blue}{$x=1$}")
svg_obj.location[0] -= 5
svg_obj.location[1] += 3



logging.info("Rendering")
bpy.context.scene.render.filepath = os.path.join(
    consts.CURRENT_PATH,
    "outputs/render.png"
)

bpy.context.scene.render.resolution_x = consts.RESOLUTION[0]
bpy.context.scene.render.resolution_y = consts.RESOLUTION[1]

log.info("Rendering image")
log.debug(f"Image size ({bpy.context.scene.render.resolution_x}, {bpy.context.scene.render.resolution_y})" )
bpy.ops.render.render(write_still=True)

log.info("Saving render blend file")
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(
    consts.CURRENT_PATH,
    "outputs/render.blend"
))


# to view render:
#  eog outputs/render.png 

# Local Variables:
# compile-command: "blender --background assets/hello_world.blend --python main.py"
# End:
