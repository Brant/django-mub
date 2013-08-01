from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.core.cache import cache

def cache_test(request):
    response_data = {
        "CSS_CACHE": cache.get("mub_css"),
        "JS_CACHE": cache.get("mub_js"),
    }
    return render_to_response("mub/test_cache.html", response_data, context_instance=RequestContext(request))
    