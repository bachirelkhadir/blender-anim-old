import os
import bpy
import subprocess as sp
from tqdm import tqdm, trange
from mathutils import Vector
import src.utils as utils
from src.consts import *
import src.tex_file_writing as tex2bpy
import src.animation_timeline as animation_timeline
import src.animations as animations
import src.basic_geometry as basic_geometry


class Scene:
    def __init__(self, quality='LOW'):
        """
        quality: enum('LOW', 'MEDIUM', 'HIGH')
        """
        self.quality = quality 
        self.fps = FPS_QUALITY[quality]
        self.engine = 'CYCLES' if quality in ('HIGH', 'VERY_HIGH') else 'BLENDER_EEVEE'
        self.last_frame = 0
        self.resolution = RESOLUTION_QUALITY[quality]
        self._setup_blender_collections()
        self._setup_timeline()

        # by default, hide all objects in collection Assets
        self._hide_all_asset_objects()

    # Add basic shapes to the scene

    def add_text(self, expression):
        text = tex2bpy.tex_to_bpy(expression,
                                  self.collections["Latex"])
        self.play(animations.Disappear(text))        
        return text

    def add_cube(self, loc=Vector([0,0,0]), scale=Vector([1,1,1]), name="Cube"):
        """
        Make cube and add it the `Creation` collection
        """
        cube = basic_geometry.make_cube(loc, scale, name)
        self.play(animations.Disappear(cube))
        self.collections["Creation"].objects.link(cube)
        return cube

    def duplicate_object(self, ob):
        copy = utils.deep_copy_object(ob)
        self.collections["Creation"].objects.link(copy)
        return copy

    def play(self, animation, duration=1):
        end_frame = self.timeline.play_animation(animation, duration)
        self.last_frame = max(self.last_frame, end_frame)

    def wait(self, duration):
        end_frame = self.timeline.wait(duration)
        self.last_frame = max(self.last_frame, end_frame)

    def render(self):
        bpy.context.scene.render.resolution_x = self.resolution[0]
        bpy.context.scene.render.resolution_y = self.resolution[1]

        # redirect output to log file
        logfile = 'blender_render.log'
        open(logfile, 'a').close()
        old = os.dup(1)
        sys.stdout.flush()
        os.close(1)
        os.open(logfile, os.O_WRONLY)

        bpy.context.scene.render.engine = self.engine
        idx = 0
        self.rendered_imgs_filepaths = []
        for frame_number in trange(0, self.last_frame, 1, desc="Rendering frame"):
            fn = f"render-frame{frame_number:02}.png"
            self.rendered_imgs_filepaths.append(fn)
            bpy.context.scene.render.filepath = os.path.join(
                CURRENT_PATH,
                f"outputs/{fn}"
            )
            bpy.context.scene.frame_set(frame_number)
            bpy.ops.render.render(write_still=True)
            idx += 1
        # disable output redirection
        os.close(1)
        os.dup(old)
        os.close(old)
        
    def write_frames_to_video(self):
        # TODO: do conversion in blender instead of ffmpeg
        # bpy.context.area.type = 'SEQUENCE_EDITOR'
        # bpy.ops.sequencer.image_strip_add(directory=os.path.join(CURRENT_PATH, OUTPUTS_DIR),
        #                                   files=[{"name": fn} for fn in self.rendered_imgs])
        # utils.save_blend_file()

        commands = [FFMPEG_BIN,
                    "-y",  # overwrite output file if it exists
                    "-r", f"{self.fps}",
                    "-f", "image2",  # input format
                    "-s", f"{self.resolution[0]}x{self.resolution[1]}",
                    "-i outputs/render-frame%02d.png",  # image name format: rende-frameXX.png
                    "-vcodec", "libx264",
                    "-crf",  "25",
                    "-pix_fmt yuv420p",
                    "-frames:v", f"{self.last_frame}",
                    "outputs/render.mp4",
                    "-loglevel", "error"]
        
        os.system(" ".join(commands))

    def open_video(self):
        commands = ["xdg-open",
                    "outputs/render.mp4"
        ]
        # commands.append("-g")
        FNULL = open(os.devnull, 'w')
        sp.call(commands, stdout=FNULL, stderr=sp.STDOUT)
        FNULL.close()



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

    def _hide_all_asset_objects(self):
        for ob in bpy.data.collections["Assets"].objects:
            self.play(animations.Disappear(ob))


