"""
URL configurations
"""
from django.conf.urls import url

from mub.views import cache_test


urlpatterns = [
    url(r'^cachetest/$', cache_test, name='mub_cache_test'),
]
