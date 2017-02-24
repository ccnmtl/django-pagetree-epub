import os

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic.base import View

from epubbuilder import epub
from pagetree.helpers import get_section_from_path
from pagetree.models import PageBlock


def is_block_allowed(block):
    return block.content_object.display_name in settings.EPUB_ALLOWED_BLOCKS


def is_image_block(block):
    return block.content_object.display_name == "Image Block"


def image_epub_filename(block):
    assert is_image_block(block)
    return "images/%d-%s" % (
        block.pk, os.path.basename(block.block().image.name))


def section_html(section):
    """ return a quick and dirty HTML version of the
    section suitable for epub """
    blocks = []
    for block in section.pageblock_set.all():
        if is_block_allowed(block):
            blocks.append(block)
        elif is_image_block(block):
            block.is_image_block = True
            block.epub_image_filename = image_epub_filename(block)
            blocks.append(block)
        else:
            block.unrenderable = True
            blocks.append(block)

    return render_to_string('epub/section.html',
                            dict(section=section, blocks=blocks))


class PageTreeRootFinder(object):
    path = "/"

    def get_root(self):
        # rely on all the defaults
        return get_section_from_path('/')


class EpubExporterView(View):
    root_finder = PageTreeRootFinder
    template_name = "epub/form.html"

    def get_root_section(self):
        rf = self.root_finder()
        return rf.get_root()

    def get(self, request):
        return render(request, self.template_name, dict())

    def post(self, request):
        root_section = self.get_root_section()

        im_book = epub.EpubBook(template_dir=settings.EPUB_TEMPLATE_DIR)

        title = settings.EPUB_TITLE
        creator = settings.EPUB_CREATOR
        publication = settings.EPUB_PUBLICATION
        im_book.setTitle(title)
        im_book.addCreator(creator)
        im_book.addMeta('date', publication,
                        event='publication')

        im_book.addTitlePage()
        im_book.addTocPage()

        # gather images from all the blocks in the site
        for pb in PageBlock.objects.filter(
                section__hierarchy=root_section.hierarchy):
            if is_image_block(pb):
                fullpath = os.path.join(settings.MEDIA_ROOT,
                                        pb.block().image.name)
                im_book.addImage(fullpath, image_epub_filename(pb))

        depth_first_traversal = root_section.get_annotated_list()
        for (i, (s, ai)) in enumerate(depth_first_traversal):
            # skip the root
            if s.is_root():
                continue
            if s.hierarchy != root_section.hierarchy:
                continue
            title = s.label
            if s.label == '':
                title = "chapter %d" % i
            n = im_book.addHtml('', '%d.html' % i,
                                section_html(s))
            im_book.addSpineItem(n)
            depth = depth_from_ai(ai)
            im_book.addTocMapNode(n.destPath, title, depth=depth)

        out = im_book.make_epub()
        resp = HttpResponse(out.getvalue(),
                            content_type="application/x-zip-compressed")
        resp['Content-Disposition'] = ("attachment; filename=%s.epub" %
                                       root_section.hierarchy.name)
        return resp


def depth_from_ai(ai):
    depth = ai['level']
    if depth == 1:
        depth = None
    return depth
