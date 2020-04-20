from contextlib import contextmanager

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Product, Category, File
from stores.utils import store_from_request
from .utils import has_file_permission_access


@contextmanager
def LogFileNotFound(*exceptions):
    try:
        yield
    except FileNotFoundError:
        pass


class FileSerializer(ModelSerializer):
    size = serializers.SerializerMethodField()
    file_type = serializers.SerializerMethodField()
    since_add = serializers.SerializerMethodField()
    file_path = serializers.SerializerMethodField()

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
        with LogFileNotFound(Exception):
            file_size = ''
            if obj.file_path and hasattr(obj.file_path, 'size'):
                file_size = obj.file_path.size
            return file_size

    def get_file_type(self, obj):
        with LogFileNotFound(Exception):
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
        with LogFileNotFound(Exception):
            files = File.objects.all().filter(product__id=obj.id)
            return FileSerializer(files, many=True, read_only=True, context=self.context).data

    class Meta:
        model = Product
        fields = ['id', 'name', 'files', 'categories', 'price']


class ProductAddSerializer(ModelSerializer):
    categories = CategorySerializer(read_only=True, many=True)
    categories_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(),
                                                       write_only=True, many=True)

    class Meta:
        model = Product
        fields = ['name',
                  'price',
                  'categories',
                  'description',
                  'categories_id']

    def create(self, validated_data):
        request = self.context.get('request')
        store = store_from_request(request)
        categories = validated_data.pop('categories_id')
        product = Product(store_id=store.id,
                          name=validated_data['name'],
                          price=validated_data['price'],
                          description=validated_data['description'])
        product.save()
        for cat in categories:
            product.categories.add(cat)
        return product


class FileUploadSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id'
    )

    class Meta:
        model = File
        read_only_fields = ('data_created', 'product')
        fields = ['id',
                  'name',
                  'price',
                  'description',
                  'order', 'product', 'file_path']
