class VGroup:
    def __init__(self, *children):
        self.children = children

    def get_children(self):
        # TODO: get children of children?
        return self.children

    def __getitem__(self, key):
        return self.children[key]

    def shift(self, s):
        for child in self.children:
            child.location += s
