from __future__ import unicode_literals

import os
from setuptools import setup

ROOT = os.path.abspath(os.path.dirname(__file__))

setup(
    name="django-pagetree-epub",
    version="0.3.0",
    author="Anders Pearson",
    author_email="ctl-dev@columbia.edu",
    url="https://github.com/ccnmtl/django-pagetree-epub",
    description="make an epub from a pagetree site",
    long_description=open(
        os.path.join(ROOT, 'README.markdown')).read(),
    install_requires=['Django>=1.8', 'nose',
                      'django-pagetree', 'epubbuilder'],
    scripts=[],
    license="BSD",
    platforms=["any"],
    zip_safe=False,
    package_data = {'': ['*.*']},
    packages=['pagetreeepub'],
    test_suite='nose.collector',
)
