import bpy
from mathutils import Vector
import src.utils as utils
from src.consts import *


class AnimationTimeline:
    def __init__(self, fps=30, anim_master_col=None):
        """
        Args:
          duration: duration of the scene in seconds
          fps: frames per second
        """

        self.fps = fps
        self.start_frame = 1
        self.end_frame = 1

        self._current_frame = 1
        self.anim_master_collection = anim_master_col


    def wait(self, duration):
        self._current_frame += self._duration_to_number_frames(duration)
        return self._current_frame

    def play_animation(self, animation, duration):
        start = self._current_frame
        end = start + self._duration_to_number_frames(duration)
        animation.setup()
        end = animation.register_animation_on_blender_timeline(start, end)
        for ob in animation.auxilary_objects:
            self.anim_master_collection.objects.link(ob)
        return end

    def _duration_to_number_frames(self, duration):
        return int(duration * self.fps)


