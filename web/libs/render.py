from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings as settings_global
#import simplejson
from django.http import HttpResponse
from django.http import HttpResponseRedirect

def render_to(template):
    def renderer(func):
        def wrapper(request, *args, **kw):
            output = func(request, *args, **kw)
            if isinstance(output, HttpResponseRedirect):
                return output
            elif isinstance(output, (list, tuple)):
                return render_to_response(output[1], output[0], RequestContext(request))
            elif isinstance(output, dict):
                return render_to_response(template, output, RequestContext(request))
            return output
        return wrapper
    return renderer

