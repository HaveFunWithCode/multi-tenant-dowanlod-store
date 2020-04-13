from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Product, Category, File


class FileSerializer(ModelSerializer):
    size = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    file_type = serializers.SerializerMethodField()
    since_add = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ('id',
                  'name',
                  'price',
                  'size',
                  'file_type',
                  'since_add')

    def get_size(self, obj):
        file_size = ''
        if obj.file_path and hasattr(obj.file_path, 'size'):
            file_size = obj.file_path.size
        return file_size

    def get_name(self, obj):
        file_name = ''
        if obj.file_path and hasattr(obj.file_path, 'name'):
            file_name = obj.file_path.name
        return file_name

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
        return FileSerializer(files,many=True,read_only=True, context=self.context).data

    class Meta:
        model = Product
        fields = ['name', 'files', 'categories', 'price']


