from mathutils import Matrix, Vector
import src.materials as materials

class VGroup:
    def __init__(self, *children, **named_children):
        self.children = [*children, *named_children.values()]
        self.named_children = named_children

    def get_children(self):
        # TODO: get children of children?
        return self.children

    def __getitem__(self, key):
        if type(key) == str:
            if key not in self.named_children:
                raise Exception(f"named child '{key}' doesn't exist in VGroup")
            return self.named_children[key]
        return self.children[key]

    def shift(self, s):
        for child in self.get_children():
            child.location += s
        return self

    def scale(self, s):
        for child in self.get_children():
            child.scale *= s
        return self

    def rotate(self, angle, around):
        for child in self.get_children():
            child.rotation_euler = (Matrix.Rotation(angle, 3, around) *child.rotation_euler.to_matrix()).to_euler()
        return self

    def set_color(self, color):
        for child in self.get_children():
            materials.color_bpy_object(child, color)
        return self

    def move_to(self, point):
        if hasattr(point, 'location'):
            point = point.location
        for child in self.get_children():
            child.location = point
        return self

    def next_to(self, point, dir=Vector([0, 0, 0]), buff=.5):
        if hasattr(point, 'location'):
            point = point.location
        for child in self.get_children():
            child.location = point + buff * dir
        return self

    def get_center(self):
        centers = [c.location for c in self.get_children()]
        # hack to take mean of vectors
        return sum(centers[1:], centers[0]) / len(centers)
