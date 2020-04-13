from .models import Store


def hostname_from_request(request):
    return request.get_host().split(':')[0].lower()


def Store_from_request(request):
    hostname = hostname_from_request(request)
    subdomain_prefix = hostname.split('.')[0]
    return Store.objects.filter(subdomain_prefix=subdomain_prefix).first()