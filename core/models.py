from django.db import models


class Contract(models.Model):
    """
    Contract Model

    A Contract is defined by a name and a date given in the form
    Is used to relate the Rates to the Contract
    A Contract can have multiple Rates
    """

    name = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return self.name


class Rate(models.Model):
    """
    Rate Model

    A Rate is defined by the origin, destination, currency, twenty, forty and fortyhc values
    Are related to a Contract
    A Rate can only have one Contract
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
