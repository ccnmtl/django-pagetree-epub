from __future__ import unicode_literals

""" run tests for pagetreeepub

$ virtualenv ve
$ ./ve/bin/pip install Django==1.8
$ ./ve/bin/pip install -r test_reqs.txt
$ ./ve/bin/python runtests.py
"""


import django
import os
from django.conf import settings
from django.core.management import call_command


def main():
    # Dynamically configure the Django settings with the minimum necessary to
    # get Django running tests
    settings.configure(
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'pagetree',
            'pagetreeepub',
            'django_jenkins',
        ),
        TEST_RUNNER='django.test.runner.DiscoverRunner',

        JENKINS_TASKS=(
            'django_jenkins.tasks.with_coverage',
        ),
        PROJECT_APPS=[
            'pagebtreeepub',
        ],
        COVERAGE_EXCLUDES_FOLDERS=['migrations'],
        ROOT_URLCONF=[],
        PAGEBLOCKS=['pagetree.TestBlock', ],
        EPUB_ALLOWED_BLOCKS=['DummyBlock'],
        EPUB_TEMPLATE_DIR=os.path.join(
            os.path.dirname(__file__), "pagetreeepub/templates/epub"),
        EPUB_TITLE='test title',
        EPUB_CREATOR='test',
        EPUB_PUBLICATION='test publication',

        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [
                    # insert your TEMPLATE_DIRS here
                ],
                'APP_DIRS': True,
                'OPTIONS': {
                    'context_processors': [
                        'django.contrib.auth.context_processors.auth',
                        'django.template.context_processors.debug',
                        'django.template.context_processors.i18n',
                        'django.template.context_processors.media',
                        'django.template.context_processors.static',
                        'django.template.context_processors.tz',
                        'django.contrib.messages.context_processors.messages',
                    ],
                },
            },
        ],

        # Django replaces this, but it still wants it. *shrugs*
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
                'HOST': '',
                'PORT': '',
                'USER': '',
                'PASSWORD': '',
            }
        }
    )

    try:
        # required by Django 1.7 and later
        django.setup()
    except AttributeError:
        pass

    # Fire off the tests
    call_command('test')


if __name__ == '__main__':
    main()
