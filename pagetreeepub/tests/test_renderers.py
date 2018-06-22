from __future__ import unicode_literals

from unittest import TestCase

from ..renderers import BaseRenderer, DefaultRenderer


class DummyBlock(object):
    def render(self):
        return "I am a Dummy Block"


class TestBaseRenderer(TestCase):
    def test_create(self):
        self.assertIsNotNone(BaseRenderer(DummyBlock()))

    def test_cant_render(self):
        r = BaseRenderer(DummyBlock())
        with self.assertRaises(NotImplementedError):
            r.render()


class TestDefaultRenderer(TestCase):
    def test_render(self):
        r = DefaultRenderer(DummyBlock())
        self.assertEqual(r.render(), "I am a Dummy Block")
