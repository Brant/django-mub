"""
URL configurations
"""
from django.conf.urls import patterns, url


urlpatterns = patterns('mub.views',
    url(r'^cachetest/$', 'cache_test', name='mub_cache_test'),
)
