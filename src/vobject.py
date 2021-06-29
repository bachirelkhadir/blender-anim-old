import src.materials as materials

class VGroup:
    def __init__(self, *children):
        names = locals().keys()
        self.children = {name: child for name, child in zip(names, children)}

    def get_children(self):
        # TODO: get children of children?
        return self.children

    def __getitem__(self, key):
        if type(key) == str:
            return self.children[key]
        return self.children.values()[key]

    def shift(self, s):
        for child in self.children.values():
            child.location += s
        return self

    def set_color(self, color):
        for child in self.children.values():
            materials.color_bpy_object(child, color)
        return self
