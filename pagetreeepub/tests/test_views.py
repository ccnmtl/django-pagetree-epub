from unittest import TestCase

from ..views import is_block_allowed, is_image_block


class DummyBlock(object):
    def __init__(self, block_name):
        self.block_name = block_name

    @property
    def content_object(self):
        class co(object):
            display_name = self.block_name
        return co()


class TestHelpers(TestCase):
    def test_is_block_allowed(self):
        d = DummyBlock("DummyBlock")
        self.assertTrue(is_block_allowed(d))
        d = DummyBlock("SomethingElse")
        self.assertFalse(is_block_allowed(d))

    def test_is_image_block(self):
        d = DummyBlock("DummyBlock")
        self.assertFalse(is_image_block(d))
        d = DummyBlock("Image Block")
        self.assertTrue(is_image_block(d))
