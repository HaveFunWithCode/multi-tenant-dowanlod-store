from django.conf import settings
from rest_framework import serializers
from .models import Store


class StoreSerializer(serializers.Serializer):
    url = serializers.SerializerMethodField(method_name='get_url')

    class Meta:
        model = Store
        fields = ['name', 'url']

    def get_url(self, obj):
        port = self.context['request'].get_port()
        return 'http://{}.{}:{}'.format(obj.subdomain_prefix, settings.BASE_DOMAIN, port)
