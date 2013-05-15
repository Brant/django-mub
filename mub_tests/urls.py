from django.conf.urls import patterns, include, url

from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="mub_tests/test.html"), name='mub_test'),
    url(r'^js/$', TemplateView.as_view(template_name="mub_tests/js_only.html"), name='mub_test_js'),
    url(r'^css/$', TemplateView.as_view(template_name="mub_tests/css_only.html"), name='mub_test_css'),
)
