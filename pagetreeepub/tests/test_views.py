from __future__ import unicode_literals

from django.test import RequestFactory
from unittest import TestCase

from ..views import (
    is_image_block, EpubExporterView, depth_from_ai)


class DummyBlock(object):
    def __init__(self, block_name):
        self.block_name = block_name

    @property
    def content_object(self):
        class co(object):
            display_name = self.block_name
        return co()


class TestHelpers(TestCase):
    def test_is_image_block(self):
        d = DummyBlock("DummyBlock")
        self.assertFalse(is_image_block(d))
        d = DummyBlock("Image Block")
        self.assertTrue(is_image_block(d))


class TestView(TestCase):
    def test_get(self):
        v = EpubExporterView.as_view()
        f = RequestFactory()
        request = f.get("/fake-path")
        response = v(request)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        v = EpubExporterView.as_view()
        f = RequestFactory()
        request = f.post("/fake-path")
        response = v(request)
        self.assertEqual(response.status_code, 200)


class TestDepthFromAI(TestCase):
    def test_depth(self):
        self.assertIsNone(depth_from_ai(dict(level=1)))
        self.assertEqual(depth_from_ai(dict(level=2)), 2)
