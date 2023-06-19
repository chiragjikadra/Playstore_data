from django.db import models


class Package(models.Model):
    name = models.CharField(max_length=100, unique=True)


class PackageDetail(models.Model):
    package = models.OneToOneField(Package, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
