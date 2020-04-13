from django.db import models
from django.utils import timezone

from stores.models import StoreAwareModel


class Category(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)

    def __str__(self):
        return self.name


class Product(StoreAwareModel):
    name = models.CharField(max_length=255, null=False, unique=True)
    categories = models.ManyToManyField(Category)
    price = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']


def content_file_name(instance, filename):
    subdomain_prefix = instance.product.store.subdomain_prefix
    return "{}/{}".format(subdomain_prefix, filename)


class File(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    file_path = models.FileField(upload_to=content_file_name)
    data_created = models.DateTimeField(default=timezone.now)
    price = models.BigIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

