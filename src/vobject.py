import src.materials as materials

class NamedChildDoesntExistInVGroupError(Exception):
    pass

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
                raise NamedChildDoesntExistInVGroupError
            return self.named_children[key]
        return self.children[key]

    def shift(self, s):
        for child in self.get_children():
            child.location += s
        return self

    def set_color(self, color):
        for child in self.get_children():
            materials.color_bpy_object(child, color)
        return self
