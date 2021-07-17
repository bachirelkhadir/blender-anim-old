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

        self._outline = []

    def wait(self, duration):
        self._current_frame += self._duration_to_number_frames(duration)
        print("-------")
        print(**locals())
        return self._current_frame

    def play_animation(self, animation, duration, start_frame=None):
        if start_frame is not None:
            start = start_frame
        else:
            start = self._current_frame

        end = start + self._duration_to_number_frames(duration)
        animation.setup()
        end = animation.register_animation_on_blender_timeline(start, end)
        for ob in animation.auxilary_objects:
            self.anim_master_collection.objects.link(ob)
        for source in animation.sources:
            s = {
                "name": source.name,
                 "animation": f"{animation}",
                 "start": start,
                "end":
                 end}
            self._outline.append(s)
        if start_frame:
            return self._current_frame
        else:
            return end

    def _duration_to_number_frames(self, duration):
        return int(duration * self.fps)



    def print_outline(self):
        from src import animation_timeline_gantt_chart
        fig = animation_timeline_gantt_chart.outline_to_gantt(self._outline)
        # TODO: change path to something meaningful
        fig.write_image("/tmp/animation_outline.png")
