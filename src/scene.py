import bpy
from mathutils import Vector
import src.utils as utils
from src.consts import *
import src.tex_file_writing as tex2bpy
import src.animation_timeline as animation_timeline
import src.basic_geometry as basic_geometry


class Scene:
    def __init__(self, fps=30):
        self.fps = fps

        self._setup_blender_collections()
        self._setup_timeline()

    # Add basic shapes to the scene

    def add_text(self, expression):
        return tex2bpy.tex_to_bpy(expression,
                                  self.collections["Latex"])

    def add_cube(self, loc=Vector([0,0,0]), scale=Vector([1,1,1]), name="Cube"):
        """
        Make cube and add it the `Creation` collection
        """
        cube = basic_geometry.make_cube(loc, scale, name)
        self.collections["Creation"].objects.link(cube)
        return cube

    def play(self, animation, duration=1):
        self.timeline.play_animation(animation, duration)

    def wait(self, duration):
        self.timeline.wait(duration)

    def _setup_blender_collections(self):
        collection_names = [("Latex", False, False),
                            ("Creation", False, False),
                            ("Animation", False, True),
                            ("Render", False, False),
        ]

        self.collections = {
            col_name: utils.create_bpy_collection(col_name, hide_viewport, hide_render)
            for col_name, hide_viewport, hide_render in collection_names
        }


    def _setup_timeline(self):
        self.timeline = animation_timeline.AnimationTimeline(self.fps, self.collections["Animation"])
