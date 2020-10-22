from django.db import models

from acc_app.models import UserAccount


class Product(models.Model):
    brand = models.CharField(max_length=30, default=None)
    name = models.CharField(max_length=30, blank=True)
    image = models.FileField(upload_to='product_image', blank=True)
    price = models.PositiveIntegerField()
    warrenty = models.CharField(max_length=10, default='30 Days')
    seller = models.ForeignKey(
        UserAccount, null=True, on_delete=models.CASCADE, blank=True)
    description = models.TextField(blank=True)
    available = models.BooleanField(default=False)
