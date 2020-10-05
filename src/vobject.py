class VGroup:
    def __init__(self, *children):
        self.children = children

    def get_children(self):
        # TODO: get children of children?
        return self.children
