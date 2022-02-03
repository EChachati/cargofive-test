from django.db import models


class Contract(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return self.name


class Rate(models.Model):
    """

    """
    origin = models.CharField(max_length=32)
    destination = models.CharField(max_length=32)
    currency = models.CharField(max_length=3)
    twenty = models.CharField(max_length=16)
    forty = models.CharField(max_length=16)
    fortyhc = models.CharField(max_length=16)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)

    def __str__(self):
        return self.origin + '-' + self.destination
