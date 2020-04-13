from django.contrib import admin
from .models import Product, File, Category
from stores.utils import store_from_request


class FileAdmin(admin.TabularInline):
    model = File
    extra = 1
    readonly_fields = ['data_created', ]
    fields = ['name',
              'price',
              'file_path',
              'data_created',
              'description', ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ['name', 'price', 'categories']
    list_display = ['name', 'price']
    readonly_fields = ['created_at']
    inlines = [FileAdmin, ]

    def get_queryset(self, request, *args, **kwargs):
        queryset = super().get_queryset(request, *args, **kwargs)
        store = store_from_request(request)
        queryset = queryset.filter(store=store)
        return queryset

    def save_model(self, request, obj, form, change):
        store = store_from_request(request)
        obj.store = store
        super().save_model(request, obj, form, change)


admin.site.register(Category)
