import sys
import os
sys.path.append(os.getcwd())

from blender_anim import *
import mathutils



class HelloWorldScene(Scene):
    def construct(self):
        lab = self.add_text_facing_camera("$f(x) = 0$")
        cube = self.add_cube()
        surf = self.add_z_function_surface("x**2+y**2")
        self.print_scene_outline()
        self.play(Appear(lab))
        # self.play(Appear(cube))
        # self.play(Appear(surf))
        self.play(Translate(lab, UP))
        self.play(Translate(surf, OUT))
        self.wait()

    def add_text_facing_camera(self, s):
        lab = self.add_text(s)
        lab.rotation_euler =  bpy.data.objects["Camera"].rotation_euler
        lab.scale = (1,1,1)
        lab.location[0] = 0
        utils.bpy_apply_transform(lab, location=False, rotation=False, scale=True)
        #color_bpy_object(lab, BABY_YELLOW)
        return lab

save_and_render(HelloWorldScene, 1, 100, engine="BLENDER_WORKBENCH")
