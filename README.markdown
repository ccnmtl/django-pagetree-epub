[![Actions Status](https://github.com/ccnmtl/django-pagetree-epub/workflows/build-and-test/badge.svg)](https://github.com/ccnmtl/django-pagetree-epub/actions)
[![Coverage Status](https://coveralls.io/repos/github/ccnmtl/django-pagetree-epub/badge.svg?branch=master)](https://coveralls.io/github/ccnmtl/django-pagetree-epub?branch=master)

epub export library for django-pagetree


## Installation

```
$ pip install django-pagetree-epub
```

Add `pagetreeepub` to your `INSTALLED_APPS`.

The `epubbuilder` library uses Genshi templates for a few things and
is unaware of Django's template finding functionality. I really hate
this and will be ripping that out and fixing this ASAP. In the
meantime, you have two options:

1) copy the `pagetreeepub/templates/epub` directory into your app and
point `EPUB_TEMPLATE_DIRECTORY` at it.
2) ensure that you pip install to a known location and set
`EPUB_TEMPLATE_DIRECTORY` to that.

Add the following settings:

* `EPUB_ALLOWED_BLOCKS` - list of pageblocks that will be allowed in
the published epub. Other blocks are silently ignored.
* `EPUB_TITLE` - title for the epub
* `EPUB_CREATOR` - creator field
* `EPUB_PUBLICATION` - publication date
