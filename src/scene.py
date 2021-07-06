import os
import abc
import bpy
from tqdm import tqdm, trange
from mathutils import Vector
import logging
import src.utils as utils
from src.consts import *
import src.tex_file_writing as tex2bpy
import src.animation_timeline as animation_timeline
import src.animations as animations
import src.basic_geometry as basic_geometry
from src.vobject import VGroup
from src.materials import color_bpy_object
from src.color_list import *


log = logging.getLogger(__name__)

class Scene:
    def __init__(self, fps=None, engine=None, resolution=None, transparent=True):
        self.fps = fps or FPS
        self.engine = engine or ENGINE
        self.resolution = resolution or RESOLUTION

        self.last_frame = 0
        self._setup_blender_collections()
        self._setup_timeline()
        self._make_transparent(transparent)

        # by default, hide all objects in collection Assets
        self._hide_all_asset_objects()

    # Add basic shapes to the scene

    def add_text(self, expression):
        text = tex2bpy.tex_to_bpy(expression,
                                  self.collections["Latex"])
        self.play(animations.Disappear(text), start_frame=0)
        return text

    def add_cube(self, loc=Vector([0,0,0]), scale=Vector([1,1,1]), name="Cube"):
        """
        Make cube and add it the `Creation` collection
        """
        cube = basic_geometry.make_cube(loc, scale, name)
        return self.add_bpy_object(cube)

    def add_plane(self, loc=Vector([0,0,0]), scale=Vector([1,1,1]), name="Plane"):
        """
        Make plane and add it the `Creation` collection
        """
        plane = basic_geometry.make_plane(loc, scale, name)
        return self.add_bpy_object(plane)

    def add_line(self, start, end, thickness, name="Line"):
        """
        Make a line
        """
        if hasattr(start, 'location'):
            start = start.location
        if hasattr(end, 'location'):
            end = end.location
        start = Vector(start)
        end = Vector(end)
        line = basic_geometry.make_line(start, end, thickness, name)
        self.add_bpy_object(line)
        return line


    def add_sphere(self, center=Vector([0, 0, 0]), radius=1., name="Sphere"):
        sphere = basic_geometry.make_sphere(center=center, radius=radius, name=name)
        self.add_bpy_object(sphere)
        return sphere

    def add_z_function_surface(self, exp_f="x**2 + y**2", name="Surf"):
        surf = basic_geometry.make_z_function_surface(exp_f, name,)
        # assign default color
        color_bpy_object(surf, BABY_PINK)
        return self.add_bpy_object(surf)


    def add_3d_axis(self, thickness.1, name="3DAxis"):
        """
        Make a 3D axis
        """
        origin = Vector((0,0,0))
        end_points = [Vector((10,0,0)), Vector((0,10,0)), Vector((0,0,10))]
        axis_lines = [self.add_line(origin, end, thickness) for end in end_points]
        colors = [ RED, BLUE, GREEN ]
        for col, ax in zip(colors, axis_lines):
           color_bpy_object(ax, col)
        axes = VGroup(*axis_lines)
        self.add(axes)
        return axes

    def add_number_plane(self, plane="XZ"):
        basis = {
            "XZ": (RIGHT, OUT),
            "XY": (RIGHT, UP),
            "YZ": (UP, OUT),
        }
        basis = basis[plane]
        lines = []
        for b1, b2 in [basis, reversed(basis)]:
            for x in range(-10, 10):
                start = x * b1 + 10*b2
                end = x * b1 - 10*b2
                line = self.add_line(start, end, 0.01 if x != 0 else 0.05)
                lines.append(line)
        return VGroup(*lines).set_color(BABY_BLUE)

    def add_bpy_object(self, obj):
        self.play(animations.Disappear(obj), start_frame=0)
        self.collections["Creation"].objects.link(obj)
        return obj

    def duplicate_object(self, ob):
        copy = utils.deep_copy_object(ob)
        self.play(animations.Disappear(copy), start_frame=0)
        self.collections["Creation"].objects.link(copy)
        return copy

    def get_copy_of_asset(self, name):
        ob = bpy.data.objects[name]
        return self.duplicate_object(ob)


    def play(self, animation, duration=1, start_frame=None):
        end_frame = self.timeline.play_animation(animation, duration,
                                                 start_frame=start_frame)
        self.last_frame = max(self.last_frame, end_frame)

    def wait(self, duration=1):
        end_frame = self.timeline.wait(duration)
        self.last_frame = max(self.last_frame, end_frame)

    def render(self, start=-1, end=-1, filename="render/render-frame", physics=False):
        if start >= end:
            logging.info(f"start >= end ({start} >= {end}), I will not render anything.")
            return
        if physics:
            log.info("Baking physics")
            bpy.ops.ptcache.bake_all()

        bpy.context.scene.render.resolution_x = self.resolution[0]
        bpy.context.scene.render.resolution_y = self.resolution[1]

        if start < 0:
            start = 0
        if end < 0:
            end = self.last_frame

        logging.info(f"engine: {self.engine}  @ {self.resolution} @ {self.fps} frames/s")
        # redirect output to log file
        logfile = 'blender_render.log'
        open(logfile, 'a').close()
        old = os.dup(1)
        sys.stdout.flush()
        os.close(1)
        os.open(logfile, os.O_WRONLY)

        bpy.context.scene.render.engine = self.engine
        bpy.context.scene.frame_start = start
        bpy.context.scene.frame_end = end
        # TODO: do we need this variable?
        self.rendered_imgs_filepaths = []

        def get_filename(frame_number):
            return f"{filename}-{frame_number:02}.png"

        log.info(f"Rendering to {get_filename(0)}")

        bar = trange(start, end, 1, desc=f"Rendering frame ({start}->{end})")
        for frame_number in bar:
            render_path = get_filename(frame_number)
            bpy.context.scene.render.filepath = render_path
            bpy.context.scene.frame_set(frame_number)
            bpy.ops.render.render(write_still=True)
        # disable output redirection
        os.close(1)
        os.dup(old)
        os.close(old)
        log.info(f"Last frame rendered: {render_path}")
        
    def write_frames_to_video(self, start=-1, end=-1):
        # TODO: do conversion in blender instead of ffmpeg
        # bpy.context.area.type = 'SEQUENCE_EDITOR'
        # bpy.ops.sequencer.image_strip_add(directory=os.path.join(CURRENT_PATH, OUTPUTS_DIR),
        #                                   files=[{"name": fn} for fn in self.rendered_imgs])
        # utils.save_blend_file()

        if start < 0:
            start = 0
        if end < 0:
            end = self.last_frame
        

        commands = [FFMPEG_BIN,
                    "-y",  # overwrite output file if it exists
                    "-r", f"{self.fps}",
                    "-f", "image2",  # input format
                    "-s", f"{self.resolution[0]}x{self.resolution[1]}",
                    "-start_number", f"{start}",
                    "-i outputs/render-frame%02d.png",  # image name format: rende-frameXX.png
                    "-vcodec", "libx264",
                    "-crf",  "25",
                    "-pix_fmt yuv420p",
                    "-frames:v", f"{end-start}",
                    "outputs/render.mp4",
                    "-loglevel", "error"]
        log.info(" ".join(commands))
        os.system(" ".join(commands))

    def open_video(self):
        commands = [XDG_OPEN,
                    "outputs/render.mp4"
        ]
        # commands.append("-g")
        utils.exec_silently(commands)

    def open_blender(self):
        commands = [BLENDER_BIN,
                    "outputs/render.blend"]
        utils.exec_silently(commands)

    def _setup_blender_collections(self):

        existing_collections = bpy.data.collections

        if bpy.data.filepath == "":
            logging.warning("Warning, no blend file specified. I will use the default blender startup file (and remove the cube).")
            objs = bpy.data.objects
            objs.remove(objs["Cube"], do_unlink=True)
            #utils.remove_bpy_collection(existing_collections["Collection"])


        collection_names = [
            ("Assets", False, False),
            ("Latex", False, False),
            ("Creation", False, False),
            ("Animation", False, True),
            ("Render", False, False),
        ]
        # create collections that don't already exist
        self.collections = {}
        for col_name, hide_viewport, hide_render in collection_names:
            col = None
            if col_name in existing_collections:
                logging.info(f"Collection {col_name} already exists!")
                col = existing_collections[col_name]
            else:
                logging.info(f"Collection {col_name} created.")
                col = utils.create_bpy_collection(col_name, hide_viewport, hide_render)
            self.collections[col_name] = col
            col.hide_viewport = hide_viewport
            col.hide_render = hide_render

    def _setup_timeline(self):
        self.timeline = animation_timeline.AnimationTimeline(self.fps, self.collections["Animation"])

    def _hide_all_asset_objects(self):
        for ob in bpy.data.collections["Assets"].objects:
            self.play(animations.Disappear(ob), start_frame=0)

    def _make_transparent(self, transparent):
        bpy.data.scenes["Scene"].render.film_transparent = transparent

    def print_scene_outline(self, include_unlinked=False):
        """
        Prints all collections and their children
        """
        if include_unlinked:
            scene_master_col = bpy.data.collections
        else:
            scene_master_col = bpy.context.scene.collection.children

        for col in scene_master_col:
            print(">", col.name)
            for obj in col.objects:
                print("\t", obj.name)


    def print_animation_outline(self):
        self.timeline.print_outline()


    def construct(self):
        raise NotImplementedError

    def add(self, ob):
        self.play(animations.Appear(ob))

    def remove(self, *obs):
        for ob in obs:
            self.play(animations.Disappear(ob))
