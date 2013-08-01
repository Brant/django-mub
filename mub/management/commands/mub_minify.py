from django.core.management.base import BaseCommand, CommandError
from django.core.cache import cache

from mub.compilers import StaticCompiler


class Command(BaseCommand):
    def handle(self, *args, **options):
        cache.delete("mub_css")
        cache.delete("mub_js")
        
        css_compiler = StaticCompiler("css")
        css_compiler.minify(lock=True)
        js_compiler = StaticCompiler("js")
        js_compiler.minify(lock=True)
        
        