from functools import wraps
from django.utils.decorators import available_attrs
from django.views.decorators.cache import cache_page

from stores.utils import store_from_request


def cache_per_store(timeout):
    """ a custom cache_page decorator to handle store based cache
     by adding store subdomain_prefix in cache_page's key_prefix arg"""

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            store = store_from_request(request)
            return cache_page(timeout, key_prefix="_store_{}_products".format(store))(view_func)(request, *args,
                                                                                                 **kwargs)

        return _wrapped_view

    return decorator
