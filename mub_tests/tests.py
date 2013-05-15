"""

"""
import os


from django.test import TestCase
from django.conf import settings
from django.test.utils import override_settings
from django.test.client import Client


class FullRequestTestCase(TestCase):
    """
    Tests relating to the full http request
    """
    def setUp(self):
        """
        Set a few things up for each test
        """
        self.client = Client()

    @override_settings(DEBUG=True)
    def test_debug_true(self):
        """
        Test spitting out both JS and CSS
        """
        resp = self.client.get("/")
        self.assertIn("/static/js/script.js", str(resp))
        self.assertIn("/static/css/style.css", str(resp))

    @override_settings(DEBUG=True)
    def test_css_debug_true(self):
        """
        Test spitting out css only
        """
        resp = self.client.get("/css/")
        self.assertIn("/static/css/style.css", str(resp))
        self.assertNotIn("/static/js/", str(resp))

    @override_settings(DEBUG=True)
    def test_js_debug_true(self):
        """
        Test spitting out JS only
        """
        resp = self.client.get("/js/")
        self.assertIn("/static/js/script.js", str(resp))
        self.assertNotIn("/static/css/", str(resp))
    
    @override_settings(DEBUG=True, MUB_MINIFY=True)
    def test_js_minify_debug_true(self):
        resp = self.client.get("/js/")
        self.assertNotIn("/static/js/script.js", str(resp))
        self.assertNotIn("/static/css/", str(resp))
        
    @override_settings(DEBUG=True, MUB_MINIFY=True)
    def test_css_minify_debug_true(self):
        resp = self.client.get("/css/")
        self.assertNotIn("/static/css/style.css", str(resp))
        self.assertNotIn("/static/js/", str(resp))
    
    @override_settings(DEBUG=True, MUB_MINIFY=True)
    def test_minify_debug_true(self):
        resp = self.client.get("/")
        self.assertNotIn("/static/css/style.css", str(resp))
        self.assertNotIn("/static/js/script.js", str(resp))
