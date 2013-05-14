"""
Template Tags for mub
"""
from django import template
from django.template.loader import render_to_string

from mub.compilers import StaticCompiler


register = template.Library()


@register.simple_tag
def add_static(ext):
    """
    Add static files to template
    """
    ext = ext.lower()
    compiler = StaticCompiler(ext)
    file_list = compiler.compile_file_list()
    return render_to_string("mub/context_%s.html" % ext, {"items": file_list})