# built-in and base renderer classes


class BaseRenderer(object):
    def __init__(self, block):
        self.block = block

    def render(self):
        raise NotImplementedError


class DefaultRenderer(BaseRenderer):
    """ Default Pageblock Renderer

    some simple pageblocks (TextBlock, HTMLBlock, etc.)
    are really simple and we don't need to do anything
    beyond just calling the block's existing .render() method
    """
    def render(self):
        return self.block.render()
