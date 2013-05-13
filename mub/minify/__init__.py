"""
Minify scripts

These are NOT my minifiers
"""
import os

from .css_min import cssmin
from .js_min import jsmin


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
        self._str = cssmin(self._str)
        
    def mini_js(self):
        """
        """
        self._str = jsmin(self._str)
        
    def save(self):
        save_dir = os.path.dirname(os.path.abspath(self._cachefile))
        if not os.path.isdir(save_dir):
            os.makedirs(save_dir)
        the_file = open(self._cachefile, "w")
        the_file.write(self._str)
        the_file.close()
    