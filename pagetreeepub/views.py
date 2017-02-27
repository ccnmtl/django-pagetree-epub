import os

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic.base import View

from epubbuilder import epub
from pagetree.helpers import get_section_from_path
from pagetree.models import PageBlock

from .renderers import DefaultRenderer


def is_image_block(block):
    return block.content_object.display_name == "Image Block"


def image_epub_filename(block):
    assert is_image_block(block)
    return "images/%d-%s" % (
        block.pk, os.path.basename(block.block().image.name))


class PageTreeRootFinder(object):
    path = "/"

    def get_root(self):
        # rely on all the defaults
        return get_section_from_path('/')


class EpubExporterView(View):
    root_finder = PageTreeRootFinder
    template_name = "epub/form.html"
    section_template = 'epub/section.html'

    def get_root_section(self):
        rf = self.root_finder()
        return rf.get_root()

    def get(self, request):
        return render(request, self.template_name, dict())

    def post(self, request):
        self.setup_renderers()
        root_section = self.get_root_section()

        im_book = epub.EpubBook(template_dir=settings.EPUB_TEMPLATE_DIR)

        im_book = self.set_epub_metadata(im_book)
        im_book = self.add_static_files_to_book(root_section.hierarchy,
                                                im_book)
        im_book = self.add_chapters(root_section, im_book)

        out = im_book.make_epub()
        resp = HttpResponse(out.getvalue(),
                            content_type="application/x-zip-compressed")
        resp['Content-Disposition'] = ("attachment; filename=%s" %
                                       self.get_epub_filename(root_section))
        return resp

    def setup_renderers(self):
        self.renderers = dict()
        # these all just get the default renderer
        for block in settings.EPUB_ALLOWED_BLOCKS:
            self.renderers[block] = DefaultRenderer
        # then merge with custom renderers
        if hasattr(settings, 'EPUB_BLOCK_RENDERERS'):
            self.renderers.update(settings.EPUB_BLOCK_RENDERERS)

    def set_epub_metadata(self, im_book):
        im_book.setTitle(self.get_title())
        im_book.addCreator(self.get_creator())
        im_book.addMeta('date', self.get_publication(),
                        event='publication')

        im_book.addTitlePage()
        im_book.addTocPage()
        return im_book

    def add_static_files_to_book(self, hierarchy, im_book):
        for pb in PageBlock.objects.filter(
                section__hierarchy=hierarchy):

            # so far, just implemented for images
            if is_image_block(pb):
                fullpath = os.path.join(settings.MEDIA_ROOT,
                                        pb.block().image.name)
                im_book.addImage(fullpath, image_epub_filename(pb))
        return im_book

    def add_chapters(self, root_section, im_book):
        depth_first_traversal = root_section.get_annotated_list()
        for (i, (s, ai)) in enumerate(depth_first_traversal):
            # skip the root
            if s.is_root():
                continue
            if s.hierarchy != root_section.hierarchy:
                continue
            title = self.title_from_section(s, i)
            n = im_book.addHtml('', '%d.html' % i, self.section_html(s))
            im_book.addSpineItem(n)
            depth = depth_from_ai(ai)
            im_book.addTocMapNode(n.destPath, title, depth=depth)
        return im_book

    def get_title(self):
        return settings.EPUB_TITLE

    def get_creator(self):
        return settings.EPUB_CREATOR

    def get_publication(self):
        return settings.EPUB_PUBLICATION

    def is_block_allowed(self, block):
        return block.content_object.display_name in self.renderers

    def get_renderer(self, block):
        return self.renderers[block.content_object.display_name](block)

    def section_html(self, section):
        blocks = []
        for block in section.pageblock_set.all():
            if self.is_block_allowed(block):
                renderer = self.get_renderer(block)
                block.epub_content = renderer.render()
                block.unrenderable = False
            else:
                block.unrenderable = True
            blocks.append(block)

        return render_to_string(self.section_template,
                                dict(section=section, blocks=blocks))

    def get_epub_filename(self, root_section):
        return "%s.epub" % root_section.hierarchy.name

    def title_from_section(self, s, i):
        title = s.label
        if s.label == '':
            title = "chapter %d" % i
        return title


def depth_from_ai(ai):
    depth = ai['level']
    if depth == 1:
        depth = None
    return depth
