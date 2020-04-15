from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Product, Category, File
from stores.utils import store_from_request
from .utils import has_file_permission_access




class FileSerializer(ModelSerializer):
    size = serializers.SerializerMethodField()
    file_type = serializers.SerializerMethodField()
    since_add = serializers.SerializerMethodField()
    file_path =serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ('id',
                  'name',
                  'price',
                  'size',
                  'file_type',
                  'since_add',
                  'file_path')
    def get_file_path(self, obj):
        request = self.context.get('request')
        if has_file_permission_access(user=request.user, fileobj=obj):
            return "http://{}{}".format(request.get_host(), obj.file_path.url)
        else:
            return "(ACESSDENIED)"


    def get_size(self, obj):
        file_size = ''
        if obj.file_path and hasattr(obj.file_path, 'size'):
            file_size = obj.file_path.size
        return file_size


    def get_file_type(self, obj):
        filename = obj.file_path.name
        return filename.split('.')[-1]

    def get_since_add(self, obj):
        date_added = obj.data_created
        return date_added


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(ModelSerializer):
    files = serializers.SerializerMethodField()
    categories = CategorySerializer(read_only=True, many=True)

    def get_files(self, obj):
        files = File.objects.all().filter(product__id=obj.id)
        return FileSerializer(files, many=True, read_only=True, context=self.context).data

    class Meta:
        model = Product
        fields = ['id', 'name', 'files', 'categories', 'price']

# class ProductAddSerializer(ModelSerializer):
#
#     categories = CategorySerializer(many=True)
#
#     class Meta:
#         model = Product
#         fields =['name', 'categories', 'price']
#
#     def create(self, validated_data):
#         request = self.context.get('request')
#
#         store_user = request.user
#         store = store_from_request(request)
#         product = ProductSerializer(store__id=store.id,
#                                     name=validated_data['name'],
#                                     price=validated_data['price'],
#                                     categories=validated_data['categories'])
#         product.save()
#         return product.id
