"""
Custom command to manually minify static files
Useful for deployment builds

manage.py mub_minify
"""
from django.core.management.base import BaseCommand, CommandError
from django.core.cache import cache

from mub.compilers import StaticCompiler
from mub.util import get_cache_key


class Command(BaseCommand):
    def handle(self, *args, **options):
        cache.delete(get_cache_key("css"))
        cache.delete(get_cache_key("js"))

        css_compiler = StaticCompiler("css")
        css_compiler.minify(lock=True)
        js_compiler = StaticCompiler("js")
        js_compiler.minify(lock=True)
