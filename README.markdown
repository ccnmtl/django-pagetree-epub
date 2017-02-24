[![Build Status](https://travis-ci.org/ccnmtl/django-pagetree-epub.png?branch=master)](https://travis-ci.org/ccnmtl/django-pagetree-epub)

epub export library for django-pagetree


## Installation

```
$ pip install django-pagetree-epub
```

Add `pagetreeepub` to your `INSTALLED_APPS`.

Add the following settings:

* `EPUB_ALLOWED_BLOCKS` - list of pageblocks that will be allowed in
the published epub. Other blocks are silently ignored.
* `EPUB_TEMPLATE_DIR` - a directory that it is safe to write files out
to (TODO: use cStringIO to avoid actually having to touch disk)
* `EPUB_TITLE` - title for the epub
* `EPUB_CREATOR` - creator field
* `EPUB_PUBLICATION` - publication date
