from rest_framework import serializers
from rest_framework.serializers import Serializer,ModelSerializer
from .models import MemberShipPlans

class MemberShipPlansSerializer(ModelSerializer):
    type = serializers.CharField(source="get_type_display")
    store_name = serializers.CharField(source="store.name", read_only=True)

    class Meta:
        model = MemberShipPlans
        fields = ["id","type","price","description","store_name"]