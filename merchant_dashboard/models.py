from django.db import models


class Product(models.Model):
    brand = models.CharField(max_length=30, default=None)
    name = models.CharField(max_length=30, blank=True)
    price = models.PositiveIntegerField()
    warrenty = models.CharField(max_length=10, default='30 Days')
    seller = models.EmailField(blank=False, null=True)
    description = models.TextField(default=name)
    available = models.BooleanField(default=False)
