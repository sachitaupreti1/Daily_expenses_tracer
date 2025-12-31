from django.db import models
from django.contrib.auth.models import User


class Expenses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    amount = models.FloatField()
    category = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return self.title


class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.CharField(max_length=200)
    amount = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return self.source
