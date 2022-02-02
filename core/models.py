from django.db import models


class Contracts(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()


class Rates(models.Model):
    """

    """
    origin = models.CharField(max_length=32)
    destination = models.CharField(max_length=32)
    currency = models.CharField(max_length=3)
    twenty = models.CharField()
    forty = models.CharField()
    fortyhc = models.CharField()
