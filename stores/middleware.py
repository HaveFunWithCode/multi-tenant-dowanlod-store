from django.conf import settings
from django.db import connection
from .utils import hostname_from_request


class SubdomainURlConfMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        subdomain = hostname_from_request(request).replace(settings.BASE_DOMAIN, '')
        if subdomain == '':
            request.urlconf = settings.BASE_URLCONF
        else:
            request.urlconf = settings.STORES_URLCONF
        return self.get_response(request)
