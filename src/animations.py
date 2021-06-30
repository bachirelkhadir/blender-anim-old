import logging
import bpy
from mathutils import Vector, Euler
import src.utils as utils
from src.consts import *
import src.basic_geometry as basic_geometry
from src.vobject import VGroup

class Animation:
    # TODO: apply animation to group of objects
    def __init__(self):
        raise NotImplementedError

    def setup(self):
        pass

    def register_animation_on_blender_timeline(self, start_frame, end_frame):
        raise NotImplementedError



# Basic transformations: Translate, Rotate, Scale
# TOD: for now, basic transformation cannot overlap with each other
class BasicTransformation(Animation):
    def __init__(self, source, delta, name_transformation='location'):
        self.sources = source.get_children() if isinstance(source, VGroup) else [source]
        self.delta = delta
        self.name_transformation = name_transformation
        self.auxilary_objects = []


    def register_animation_on_blender_timeline(self, start_frame, end_frame):
        for source in self.sources:
            name_transformation = self.name_transformation
            bpy.context.scene.frame_set(start_frame)
            source.keyframe_insert(data_path=name_transformation, index=-1)

            bpy.context.scene.frame_set(end_frame)
            object_pose = getattr(source, name_transformation)
            for i, delta_i in enumerate(self.delta):
                object_pose[i] += delta_i
            source.keyframe_insert(data_path=name_transformation, index=-1)
        return end_frame


class Rotate(BasicTransformation):
    # Fix rotation axis
    def __init__(self, source, euler_rotation):
        super().__init__(source, euler_rotation, "rotation_euler")


class Translate(BasicTransformation):
    def __init__(self, source, shift):
        super().__init__(source, shift, "location")

    def register_animation_on_blender_timeline(self, start_frame, end_frame):
        name_transformation = self.name_transformation


        def keyframe_insert_all():
            for source in self.sources:
                # Save loc+rot+scale because a global scaling can affect all of
                # those
                for data_path in ('scale', 'location', 'rotation_euler'):
                    source.keyframe_insert(data_path=data_path, index=-1)

        bpy.context.scene.frame_set(start_frame)
        keyframe_insert_all()

        # Select all
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = self.sources[0]
        for source in self.sources:
            source.select_set(state=True)

        bpy.context.scene.frame_set(end_frame)

        # resize all objects using ops
        # bpy.ops.transform.resize(value=self.delta)
        bpy.ops.transform.translate(value=self.delta, orient_type='GLOBAL',
                                    orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                                    orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False,
                                    proportional_edit_falloff='SMOOTH', proportional_size=1,
                                    use_proportional_connected=False, use_proportional_projected=False)


        keyframe_insert_all()
        return end_frame


class Scale(BasicTransformation):
    def __init__(self, source, scale):
        super().__init__(source, scale, "scale")

    def register_animation_on_blender_timeline(self, start_frame, end_frame):
        name_transformation = self.name_transformation


        def keyframe_insert_all():
            for source in self.sources:
                # Save loc+rot+scale because a global scaling can affect all of
                # those
                for data_path in ('scale', 'location', 'rotation_euler'):
                    source.keyframe_insert(data_path=data_path, index=-1)

        bpy.context.scene.frame_set(start_frame)
        keyframe_insert_all()

        # Select all
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = self.sources[0]
        for source in self.sources:
            source.select_set(state=True)

        bpy.context.scene.frame_set(end_frame)

        # resize all objects using ops
        # bpy.ops.transform.resize(value=self.delta)
        bpy.ops.transform.resize(value=self.delta, orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)


        keyframe_insert_all()
        return end_frame

class Appear(Animation):
    def __init__(self, source):
        self.sources = source.get_children() if isinstance(source, VGroup) else [source]
        self.auxilary_objects = []

    def register_animation_on_blender_timeline(self, start_frame, _):
        for source in self.sources:
            source.hide_render = 0
            source.keyframe_insert(data_path="hide_render", frame=start_frame)
        return start_frame


class Disappear(Animation):
    def __init__(self, source):
        self.sources = source.get_children() if isinstance(source, VGroup) else [source]
        self.auxilary_objects = []

    def register_animation_on_blender_timeline(self, start_frame, _):
        for source in self.sources:
            source.hide_render = 1
            source.keyframe_insert(data_path="hide_render", frame=start_frame)
        return start_frame





class WrapInto(Animation):
    def __init__(self, source, target):
        self.source = source
        self.target = target
        self.auxilary_objects = []


    def setup(self):
        source = self.source
        target = self.target

        target_name = target.name
        target_copy = utils.deep_copy_object(target)
        target_copy.name = target_name + '-target'
        target_copy.location = source.location

        modifier = source.modifiers.new("Shrinkwrap", 'SHRINKWRAP')
        modifier.target = target_copy

        # add shirnk modifier
        # todo: bypass bpy.ops
        bpy.context.view_layer.objects.active = source
        bpy.ops.object.modifier_apply_as_shapekey(modifier=modifier.name, keep_modifier=False)

        self.auxilary_objects.append(target_copy)


    def register_animation_on_blender_timeline(self, start_frame, end_frame):
        # interpolate between shrink=0 and shrink=1
        shrink_shape_key = self.source.data.shape_keys.key_blocks['Shrinkwrap']
        shrink_shape_key.value = 0
        shrink_shape_key.keyframe_insert(data_path="value", frame=start_frame)
        shrink_shape_key.value = 1
        shrink_shape_key.keyframe_insert(data_path="value", frame=end_frame)
        return end_frame


class CubeOverlap(Animation):
    def __init__(self, source, direction='x', appear=True):
        self.source = source
        self.direction = direction
        self.appear = appear
        self.auxilary_objects = []

    def setup(self):
        # Make cube
        source = self.source
        loc, scale = utils.get_aligned_bounding_box(source)
        cube = basic_geometry.make_cube(loc, scale)
        cube.name = f"Cube Hide {source.name}"
        cube.display_type = 'WIRE'
        self.hiding_cube = cube

        # add boolean modifier
        modifier = source.modifiers.new("Boolean", type='BOOLEAN')
        modifier.operation = 'DIFFERENCE'
        modifier.object = cube

        self.auxilary_objects.append(cube)


    def register_animation_on_blender_timeline(self, start_frame, end_frame):
        appear = self.appear
        cube = self.hiding_cube
        direction = self.direction

        idx_direction = {'x': 0, 'y': 1, 'z': 2}[direction]

        # Slide cube along `direction` to hide/show object
        bpy.context.scene.frame_set(start_frame)
        if not appear:
            cube.location[idx_direction] += cube.dimensions[idx_direction]
        cube.keyframe_insert(data_path="location", index=-1)

        bpy.context.scene.frame_set(end_frame)
        cube.location[idx_direction] -= cube.dimensions[idx_direction]
        cube.keyframe_insert(data_path="location", index=-1)
        return end_frame


class GraduallyDisappear(CubeOverlap):
    def __init__(self, source, direction='x'):
        super().__init__(source, direction, appear=False)


class GraduallyAppear(CubeOverlap):
    def __init__(self, source, direction='x'):
        super().__init__(source, direction, appear=True)


class AnimateShapeKey(Animation):
    def __init__(self, source, key_name, start_value, end_value):
        self.source = source
        self.sources = [source]
        self.start_value = start_value
        self.end_value = end_value
        self.key_name = key_name
        self.auxilary_objects = []



    def register_animation_on_blender_timeline(self, start_frame, end_frame):
        logging.info(f"Animate keyframe {start_frame} --> {end_frame}")
        # interpolate between start and end value
        if not self.source.data.shape_keys:
            raise Exception(f"Object '{self.source.name}' doesn't have shape keys")
        if self.key_name not in self.source.data.shape_keys.key_blocks:
            logging.error(f"{self.key_name} is not a valid shape key for {self.source.name}. Available keys: {self.source.data.shape_keys.key_blocks.items()}")
            raise Exception(f"{self.key_name} is not a valid shape key for {self.source.name}")
        shape_key = self.source.data.shape_keys.key_blocks[self.key_name]
        shape_key.value = self.start_value
        shape_key.keyframe_insert(data_path="value", frame=start_frame)
        shape_key.value = self.end_value
        shape_key.keyframe_insert(data_path="value", frame=end_frame)
        return end_frame
