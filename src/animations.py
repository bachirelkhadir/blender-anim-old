import bpy
from mathutils import Vector
import src.utils as utils
from src.consts import *


class WrapInto:
    def __init__(self, source, target, start_frame=1, end_frame=30):
        
        target_name = target.name
        target_copy = target.copy()
        target_copy.data = target.data.copy()
        target_copy.animation_data_clear()
        if target_copy.data.shape_keys:
           target_copy.data.shape_keys.animation_data_clear()
        
        target_copy.name = target_name + '-target'
        target_copy.location = source.location
        bpy.context.collection.objects.link(target_copy)
        target_copy.hide_render = True


        modifier = source.modifiers.new("Shrinkwrap", 'SHRINKWRAP')
        modifier.target = target_copy

        # add shirnk modifier
        # todo: bypass bpy.ops
        bpy.context.view_layer.objects.active = source
        bpy.ops.object.modifier_apply_as_shapekey(modifier=modifier.name, keep_modifier=False)

        # interpolate between shrink=0 and shrink=1
        shrink_shape_key = source.data.shape_keys.key_blocks['Shrinkwrap']
        shrink_shape_key.value = 0
        shrink_shape_key.keyframe_insert(data_path="value", frame=start_frame)
        shrink_shape_key.value = 1
        shrink_shape_key.keyframe_insert(data_path="value", frame=end_frame)

        target_copy.location[1] += 3



class CubeOverlap:
    def __init__(self, source, direction='x', appear=True, start_frame=1, end_frame=30):
        idx_direction = {'x': 0, 'y': 1, 'z': 2}[direction]
        
        loc, scale = utils.get_aligned_bounding_box(source)

        cube = utils.make_cube(loc, scale)
        cube.name = f"Cube Hide {source.name}"
        bpy.context.collection.objects.link(cube)
        cube.hide_render = True

        # add boolean modifier
        modifier = source.modifiers.new("Boolean", type='BOOLEAN')
        modifier.operation = 'DIFFERENCE'
        modifier.object = cube



        bpy.context.scene.frame_set(start_frame)
        if not appear:
            cube.location[idx_direction] += scale[idx_direction]
        cube.keyframe_insert(data_path="location", index=-1)


        bpy.context.scene.frame_set(end_frame)
        cube.location[idx_direction] -= scale[idx_direction]
        cube.keyframe_insert(data_path="location", index=-1)


class Disappear(CubeOverlap):
    def __init__(self, source, direction='x', start_frame=1, end_frame=30):
        super(Disappear, self).__init__(source, direction, appear=False, start_frame=start_frame, end_frame=end_frame)


class Appear(CubeOverlap):
    def __init__(self, source, direction='x', start_frame=1, end_frame=30):
        super(Appear, self).__init__(source, direction, appear=True,  start_frame=start_frame, end_frame=end_frame)
