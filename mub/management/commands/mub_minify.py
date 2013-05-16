from django.core.management.base import BaseCommand, CommandError

from mub.compilers import StaticCompiler

class Command(BaseCommand):
    def handle(self, *args, **options):
        css_compiler = StaticCompiler("css")
        css_compiler.minify()
        js_compiler = StaticCompiler("js")
        js_compiler.minify()