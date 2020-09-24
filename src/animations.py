import bpy
from mathutils import Vector, Euler
import src.utils as utils
from src.consts import *
import src.basic_geometry as basic_geometry


class Animation:
    # TODO: apply animation to group of objects
    def __init__(self):
        raise NotImplementedError

    def setup(self):
        pass

    def register_animation_on_blender_timeline(self, start_frame, end_frame):
        raise NotImplementedError


# Basic transformations: Translate, Rotate, Scale
class BasicTransformation(Animation):
    def __init__(self, source, delta, name_transformation='location'):
        self.source = source
        self.delta = delta
        self.name_transformation = name_transformation
        self.auxilary_objects = []


    def register_animation_on_blender_timeline(self, start_frame, end_frame):
        name_transformation = self.name_transformation
        bpy.context.scene.frame_set(start_frame)
        self.source.keyframe_insert(data_path=name_transformation, index=-1)

        bpy.context.scene.frame_set(end_frame)
        object_pose = getattr(self.source, name_transformation)
        for i, delta_i in enumerate(self.delta):
             object_pose[i] += delta_i
        self.source.keyframe_insert(data_path=name_transformation, index=-1)


class Rotate(BasicTransformation):
    def __init__(self, source, euler_rotation):
        super().__init__(source, euler_rotation, "rotation_euler")


class Translate(BasicTransformation):
    def __init__(self, source, shift):
        super().__init__(source, shift, "location")


class Scale(BasicTransformation):
    def __init__(self, source, scale):
        super().__init__(source, scale, "scale")


class Appear(Animation):
    def __init__(self, source):
        self.source = source
        self.auxilary_objects = []

    def register_animation_on_blender_timeline(self, start_frame, _):
        self.source.hide_render = 0
        self.source.keyframe_insert(data_path="hide_render", frame=start_frame)


class Disappear(Animation):
    def __init__(self, source):
        self.source = source
        self.auxilary_objects = []

    def register_animation_on_blender_timeline(self, start_frame, _):
        self.source.hide_render = 1
        self.source.keyframe_insert(data_path="hide_render", frame=start_frame)


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


class GraduallyDisappear(CubeOverlap):
    def __init__(self, source, direction='x'):
        super(Disappear, self).__init__(source, direction, appear=False)


class GraduallyAppear(CubeOverlap):
    def __init__(self, source, direction='x'):
        super(Appear, self).__init__(source, direction, appear=True)




