"""

"""
import os
import shutil

from django.test import TestCase
from django.conf import settings
from django.test.utils import override_settings
from django.test.client import Client
from django.core.management import call_command

from mub.compilers import StaticCompiler


class CleanableCache(TestCase):
    """
    Standardize setup/teardown across tests
    """
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

    def tearDown(self):
        """
        Clean things up after each test
        """
        self.css_compiler.clean_up()
        self.js_compiler.clean_up()
        self._assert_clean()

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

    def remove_static_root(self):
        """
        Clear collectstatic location
        """
        if os.path.isdir(settings.STATIC_ROOT):
            shutil.rmtree(settings.STATIC_ROOT)


class MiscTestCase(CleanableCache):
    """
    Just some miscellaneous stuff
    """
    @override_settings(STATIC_ROOT=settings.STATIC_ROOT + "/", DEBUG=False)
    def setUp(self):
        """
        Collect static
        """
        call_command("collectstatic", interactive=False)
    
    @override_settings(STATIC_ROOT=settings.STATIC_ROOT + "/", DEBUG=False)
    def tearDown(self):
        """
        Remove static root
        """
        shutil.rmtree(settings.STATIC_ROOT)
    
    @override_settings(STATIC_ROOT=settings.STATIC_ROOT + "/", DEBUG=False)
    def test_appended_slash(self):
        """
        Make sure we are all good if static root has an appending slash
        
        This is really just a code coverage thing
        """
        resp = self.client.get("/")


class FullRequestDebugFalseTestCase(CleanableCache):
    """
    Tests relating to the full http request
    while DEBUG is False
    """
    @override_settings(DEBUG=False)
    def setUp(self):
        """
        Some setup before each test
        """
        if os.path.isdir(settings.STATIC_ROOT):
            shutil.rmtree(settings.STATIC_ROOT)
        self.assertFalse(os.path.isdir(settings.STATIC_ROOT))
        call_command("collectstatic", interactive=False)
        self.assertTrue(os.path.isdir(settings.STATIC_ROOT))
        super(FullRequestDebugFalseTestCase, self).setUp()
        self.assertIn(settings.STATIC_ROOT, self.css_compiler.cache_location)
        self.assertIn(settings.STATIC_ROOT, self.js_compiler.cache_location)
    
    def tearDown(self):
        """
        Remove cache dirs and STATIC_ROOT
        """
        super(FullRequestDebugFalseTestCase, self).tearDown()
        shutil.rmtree(settings.STATIC_ROOT)
        self.assertFalse(os.path.isdir(settings.STATIC_ROOT))
    
    def test_css_minify(self):
        """
        Test spitting out css only
        """
        resp = self.client.get("/css/")
        self.assertNotIn("/static/css/style.css", str(resp))
        self.assertNotIn("/static/js/", str(resp))
        self.assertIn("/static/css/cache", str(resp))
        self.assertNotIn("/static/js/cache", str(resp))
        self._assert_cache_exists("css")
        
    def test_js_minify(self):
        """
        Test spitting out js only
        """
        resp = self.client.get("/js/")
        self.assertNotIn("/static/css/", str(resp))
        self.assertNotIn("/static/js/script.js", str(resp))
        self.assertIn("/static/js/cache", str(resp))
        self.assertNotIn("/static/css/cache", str(resp))
        self._assert_cache_exists("js")
    
    def test_minify(self):
        """
        Test spitting out css only
        """
        resp = self.client.get("/")
        self.assertNotIn("/static/css/style.css", str(resp))
        self.assertNotIn("/static/js/script.js", str(resp))
        self.assertIn("/static/js/cache", str(resp))
        self.assertIn("/static/css/cache", str(resp))
        self._assert_cache_exists("css")
        self._assert_cache_exists("js")



class FullRequestDebugTrueTestCase(CleanableCache):
    """
    Tests relating to the full http request
    while DEBUG is True
    """
    @override_settings(DEBUG=True)
    def setUp(self):
        """
        Some setup before each test
        """
        super(FullRequestDebugTrueTestCase, self).setUp()
        self.assertNotIn(self.css_compiler.cache_location, settings.STATIC_ROOT)
        self.assertNotIn(self.js_compiler.cache_location, settings.STATIC_ROOT)
        self.assertFalse(os.path.isdir(settings.STATIC_ROOT))
    
    @override_settings(DEBUG=True)
    def tearDown(self):
        """
        clear out stuff we've put places after each test
        """
        super(FullRequestDebugTrueTestCase, self).tearDown()

    @override_settings(DEBUG=True)
    def test_debug_true(self):
        """
        Test spitting out both JS and CSS as individual items
        """
        resp = self.client.get("/")
        self.assertIn("/static/js/script.js", str(resp))
        self.assertIn("/static/css/style.css", str(resp))
        self._assert_clean()

      
    
    @override_settings(DEBUG=True)
    def test_css_debug_true(self):
        """
        Test spitting out css only as individual items
        """
        resp = self.client.get("/css/")
        self.assertIn("/static/css/style.css", str(resp))
        self.assertNotIn("/static/js/", str(resp))
        self._assert_clean()

    @override_settings(DEBUG=True)
    def test_js_debug_true(self):
        """
        Test spitting out JS only as individual items
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


class CSSOrderingTestCase(CleanableCache):
    """
    Test cases relating to properly ordering css files
    """
    @override_settings(DEBUG=True)
    def setUp(self):
        """
        Some setup before each test
        """
        super(CSSOrderingTestCase, self).setUp()
        
    @override_settings(DEBUG=True)
    def tearDown(self):
        """
        clear out stuff we've put places after each test
        """
        super(CSSOrderingTestCase, self).tearDown()
        
    @override_settings(DEBUG=True, MUB_CSS_ORDER=(("style.css", "style-2.css"), ()))
    def test_css_ordering_1(self):
        resp = self.client.get("/css/")
        self.assertIn("/static/css/style.css", str(resp))
        self.assertTrue(str(resp).index("style.css") < str(resp).index("style-2.css"))
        self.assertTrue(str(resp).index("style.css") < str(resp).index("style-3.css"))
        self.assertTrue(str(resp).index("style-2.css") < str(resp).index("style-3.css"))
        
    @override_settings(DEBUG=True, MUB_CSS_ORDER=(("style-2.css", "style.css"), ()))
    def test_css_ordering_2(self):
        resp = self.client.get("/css/")
        self.assertIn("/static/css/style.css", str(resp))
        self.assertTrue(str(resp).index("style-2.css") < str(resp).index("style.css"))
        self.assertTrue(str(resp).index("style.css") < str(resp).index("style-3.css"))
        self.assertTrue(str(resp).index("style-2.css") < str(resp).index("style-3.css"))
    
    @override_settings(DEBUG=True, MUB_CSS_ORDER=(("style-2.css", "style.css"), ("style-3.css", )))
    def test_css_ordering_3(self):
        resp = self.client.get("/css/")
        self.assertIn("/static/css/style.css", str(resp))
        self.assertTrue(str(resp).index("style-2.css") < str(resp).index("style.css"))
        self.assertTrue(str(resp).index("style.css") < str(resp).index("style-3.css"))
        self.assertTrue(str(resp).index("style-2.css") < str(resp).index("style-3.css"))  
    
    @override_settings(DEBUG=True, MUB_CSS_ORDER=(("style-2.css", "style.css"), ("style-3.css", )))
    def test_css_ordering_4(self):
        resp = self.client.get("/css/")
        self.assertIn("/static/css/style.css", str(resp))
        self.assertTrue(str(resp).index("style-2.css") < str(resp).index("style.css"))
        self.assertTrue(str(resp).index("style.css") < str(resp).index("style-3.css"))
        self.assertTrue(str(resp).index("style-2.css") < str(resp).index("style-3.css"))

    @override_settings(DEBUG=True, MUB_CSS_ORDER=(("style-3.css", "style.css"), ("style-2.css", )))
    def test_css_ordering_5(self):
        resp = self.client.get("/css/")
        self.assertIn("/static/css/style.css", str(resp))
        self.assertTrue(str(resp).index("style-3.css") < str(resp).index("style.css"))
        self.assertTrue(str(resp).index("style.css") < str(resp).index("style-2.css"))
        self.assertTrue(str(resp).index("style-3.css") < str(resp).index("style-2.css"))
    
    @override_settings(DEBUG=True, MUB_CSS_ORDER=((), ("style-2.css", )))
    def test_css_ordering_6(self):
        resp = self.client.get("/css/")
        self.assertIn("/static/css/style.css", str(resp))
        self.assertTrue(str(resp).index("style-3.css") < str(resp).index("style-2.css"))
        self.assertTrue(str(resp).index("style.css") < str(resp).index("style-2.css"))
    
    
    