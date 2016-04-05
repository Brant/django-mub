"""
Minify scripts

The actual minify scripts are NOT my minifiers
"""
import os

from django.conf import settings
from django.template.loader import render_to_string
from django.utils.encoding import smart_unicode

from .css_min import cssmin
from .js_min import jsmin
from mub.util import massage_css_images_for_cache_path

class MUBMinifier:

    def __call__(self, ext, filelist, cachefile):
        self._filelist = filelist
        self._cachefile = cachefile
        self._ext = ext
        self._str = ""
        self.build_string()
        mini_method = getattr(self, "mini_%s" % self._ext)
        mini_method()
        self.save()

    def build_string(self):
        for filename, location in self._filelist:
            the_file = open(os.path.join(location, filename))
            self._str += the_file.read()
            the_file.close()

    def mini_css(self):
        """
        """
        css_url = settings.STATIC_URL + os.sep.join(self._filelist[0][0].split(os.sep)[:-1])
        self._str = cssmin(massage_css_images_for_cache_path(smart_unicode(self._str), css_url))

    def mini_js(self):
        """
        """
        self._str = jsmin(render_to_string("mub/js_config.txt", {"STATIC_URL": settings.STATIC_URL}) + smart_unicode(self._str))


    def save(self):
        save_dir = os.path.dirname(os.path.abspath(self._cachefile))
        if not os.path.isdir(save_dir):
            os.makedirs(save_dir)
        the_file = open(self._cachefile, "w")
        the_file.write(self._str)
        the_file.close()

