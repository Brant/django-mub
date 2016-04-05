#!/usr/bin/env python
import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

MY_INSTALLED_APPS = [
    'mub',
    'mub_tests',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

if not settings.configured:
    settings.configure(
        BASE_DIR = BASE_DIR,
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
        STATICFILES_DIRS = (PROJECT_PATH + "/static", ),
        STATICFILES_FINDERS = (
            'django.contrib.staticfiles.finders.FileSystemFinder',
        ),
        INSTALLED_APPS = MY_INSTALLED_APPS,
        SITE_ID = 1,
        STATIC_URL = '/static/',
        STATIC_ROOT = PROJECT_PATH + "/collectstatic",
        ROOT_URLCONF = 'mub_tests.urls',
        TEST_RUNNER = 'django.test.runner.DiscoverRunner',
    )


def runtests():
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["mub_tests"])
    sys.exit(bool(failures))


if __name__ == '__main__':
    runtests(*sys.argv[1:])
