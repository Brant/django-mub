"""

"""
import os


from django.test import TestCase
from django.conf import settings
from django.test.utils import override_settings
from django.test.client import Client

from mub.compilers import StaticCompiler


class FullRequestDebugTrueTestCase(TestCase):
    """
    Tests relating to the full http request
    """
    @override_settings(DEBUG=True)
    def setUp(self):
        """
        Set a few things up for each test
        """
        self.css_compiler = StaticCompiler("css")
        self.js_compiler = StaticCompiler("js")
        self.client = Client()
        self.css_compiler.clean_up()
        self.js_compiler.clean_up()
        self._assert_clean()
        self.assertNotIn(self.css_compiler.cache_location, settings.STATIC_ROOT)
        self.assertNotIn(self.js_compiler.cache_location, settings.STATIC_ROOT)
    
    def _assert_clean(self):
        """
        Assert that the cache dirs do not exist
        """
        self.assertFalse(os.path.isdir(self.css_compiler.cache_location))
        self.assertFalse(os.path.isdir(self.js_compiler.cache_location))
    
    def _assert_cache_exists(self, ext):
        """
        Assert that the cache dir exists
        """
        compiler = getattr(self, "%s_compiler" % ext)
        self.assertTrue(os.path.isdir(compiler.cache_location))
    
    @override_settings(DEBUG=True)
    def tearDown(self):
        self.css_compiler.clean_up()
        self.js_compiler.clean_up()
        self._assert_clean()

    @override_settings(DEBUG=True)
    def test_debug_true(self):
        """
        Test spitting out both JS and CSS
        """
        resp = self.client.get("/")
        self.assertIn("/static/js/script.js", str(resp))
        self.assertIn("/static/css/style.css", str(resp))
        self._assert_clean()

    @override_settings(DEBUG=True)
    def test_css_debug_true(self):
        """
        Test spitting out css only
        """
        resp = self.client.get("/css/")
        self.assertIn("/static/css/style.css", str(resp))
        self.assertNotIn("/static/js/", str(resp))
        self._assert_clean()

    @override_settings(DEBUG=True)
    def test_js_debug_true(self):
        """
        Test spitting out JS only
        """
        resp = self.client.get("/js/")
        self.assertIn("/static/js/script.js", str(resp))
        self.assertNotIn("/static/css/", str(resp))
        self._assert_clean()
    
    @override_settings(DEBUG=True, MUB_MINIFY=True)
    def test_js_minify_debug_true(self):
        resp = self.client.get("/js/")
        self.assertNotIn("/static/js/script.js", str(resp))
        self.assertNotIn("/static/css/", str(resp))
        self._assert_cache_exists("js")
        
    @override_settings(DEBUG=True, MUB_MINIFY=True)
    def test_css_minify_debug_true(self):
        resp = self.client.get("/css/")
        self.assertNotIn("/static/css/style.css", str(resp))
        self.assertNotIn("/static/js/", str(resp))
        self._assert_cache_exists("css")
    
    @override_settings(DEBUG=True, MUB_MINIFY=True)
    def test_minify_debug_true(self):
        resp = self.client.get("/")
        self.assertNotIn("/static/css/style.css", str(resp))
        self.assertNotIn("/static/js/script.js", str(resp))
        self._assert_cache_exists("js")
        self._assert_cache_exists("css")
