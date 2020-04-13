from django.db import models


class Store(models.Model):
    name = models.CharField(max_length=100)
    subdomain_prefix = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class StoreAwareModel(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    class Meta:
        abstract = True
