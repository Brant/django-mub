"""
Static file list compilers
"""
import os
import shutil

from django.contrib.staticfiles.finders import FileSystemFinder
from django.conf import settings
from django.contrib.staticfiles.utils import get_files

from mub.minify import MUBMinifier
from mub.util import latest_timestamp


class StaticCompiler(object):
    """
    Handle compiling the list of static file paths
    """
    def __init__(self, ext):
        """
        Initialize with the extension (e.g. 'js' or 'css')
        """
        self._ext = ext
        self._items = {}
        self._ordered_items = []
        self._filename = None
        self._timestamp = None
        self._location = None
        self.cache_location = None
        self._compile_file_list()
        self.is_minified = False
    
    def _compile_file_list_from_staticfiles_dirs(self):
        """
        Compile list of static files for the given extension
        
        Used when serving out of STATICFILES_DIRS (i.e. DEBUG = True)
        """
        finder = FileSystemFinder()

        for path, storage in finder.list(ignore_patterns=None):
            if path.endswith(".%s" % self._ext) and path.count(os.sep) < 2:
                self._items.update({path.split(os.sep)[-1]: (path, storage.location)})        

    def _compile_file_list_from_static_root(self):
        """
        Compile list of statif files for the given extension
        
        Used when serving out of STATIC_ROOT (i.e. DEBUG = False)
        """
        dir_list = []
        rootdir = settings.STATIC_ROOT
        
        if rootdir.endswith("/") or rootdir.endswith("\\"):
            rootdir = rootdir[:-1]
            
        for root, subFolders, files in os.walk(rootdir):
            if root.replace(rootdir, "").count(os.sep) == 1:
                dir_list.append((root.replace("%s%s" % (rootdir, os.sep), ""), [a_file for a_file in files if a_file.endswith(".%s" % self._ext)]))
        
        useable_list = []
        
        for item in dir_list:
            if len(item[1]) > 0:
                useable_list.append(item)
        
        final_dict = {}
        for path, items in useable_list:
            for item in items:
                final_dict.update({u"%s" % item: (u"%s/%s" % (path, item), rootdir)})
        self._items = final_dict

    def clean_up(self):
        if self.cache_location and os.path.isdir(self.cache_location):
            shutil.rmtree(self.cache_location)
    
    def get_staticfiles_list(self):
        """
        Return list of static files to serve
        """
        self._massage_ordered_list()
        return [item[0] for item in self._ordered_items]
    
    def _compile_file_list(self):
        """
        Return the list of files to feed to the template
        """
        if settings.DEBUG:
            self._compile_file_list_from_staticfiles_dirs()
        else:
            self._compile_file_list_from_static_root()
        
        if self._items:
            self._location = self._items.values()[0][1]
      
            cache_location = self._items.values()[0][0]
            cache_location = cache_location.split("/")
            cache_location[len(cache_location)-1] = "cache"
      
            self._cache_path = "/".join(cache_location) + "/"
            self.cache_location = os.path.join(self._location, self._cache_path)
      
            self.order_file_list()

    def order_file_list(self):
        """
        Place the items in an order (if one exists)
        """
        params = getattr(settings, "MUB_%s_ORDER" % self._ext.upper(), ((), ()))
        top_files = params[0]
        bottom_files = params[1]
        
        for filename in top_files:
            if filename in self._items:
                self._ordered_items.append(self._items[filename])
                del self._items[filename]
        
        for_bottom = []
        for filename in bottom_files:
            if filename in self._items:
                for_bottom.append(self._items[filename])
                del self._items[filename]

        for filename in self._items:
            self._ordered_items.append(self._items[filename])

        self._ordered_items += for_bottom

    def _massage_ordered_list(self):
        """
        Do some stuff with the ordered list before shipping it out
        """
        if self._ordered_items and getattr(settings, "MUB_MINIFY", (not settings.DEBUG)):
            self.minify()
            self.is_minified = True

    def minify(self):
        """
        Responsible for minifying
        """
        self._timestamp = latest_timestamp([os.path.join(location, path) for path, location in self._ordered_items])
        self._establish_filename()

        cachefile = os.path.join(self.cache_location, self._filename)

        if not os.path.isfile(cachefile):
            minifier = MUBMinifier()
            minifier(self._ext, self._ordered_items, cachefile)

        self._ordered_items = [("%s%s" % (self._cache_path, self._filename), self.cache_location)]

    def _establish_filename(self):
        """
        returns a filename based on a timestamp
        """
        self._filename = "%s-%s_.%s" % (self._ext, str(self._timestamp), self._ext)
