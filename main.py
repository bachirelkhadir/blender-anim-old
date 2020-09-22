import os
import sys
import hashlib
from pathlib import Path
from random import randint
import bpy
sys.path.append(os.path.dirname(os.path.dirname(bpy.data.filepath)))

print(sys.path)
import src.tex_file_writing as tex2bpy
import src.consts as consts






ob = bpy.data.objects["Sphere"]
frame_number = 0


svg_obj = tex2bpy.tex_to_bpy(r"the equation $x = 1$")
svg_obj.location[0] -= 3

svg_obj = tex2bpy.tex_to_bpy(r"the equation $x = 7$")
svg_obj.location[0] -= 5
svg_obj.location[1] += 3



print("Rendering")
bpy.context.scene.render.filepath = os.path.join(
    consts.CURRENT_PATH,
    "outputs/render.png"
)

bpy.context.scene.render.resolution_x = 800
bpy.context.scene.render.resolution_y = 600
bpy.ops.render.render(write_still=True)

print("Saving to", type(os.path.join(
    consts.CURRENT_PATH,
    "outputs/render.blend"
)))

print(type(bpy.data.filepath))


bpy.ops.wm.save_as_mainfile(filepath=os.path.join(
    consts.CURRENT_PATH,
    "outputs/render.blend"
))



# Local Variables:
# compile-command: "blender --background assets/hello_world.blend --python main.py"
# End:
