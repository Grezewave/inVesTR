# Create your models here.
from django.db import models


class Investment(models.Model):
    current_value = models.DecimalField(max_digits=10, decimal_places=2)
    investment_code = models.CharField(max_length=50)
    institution = models.CharField(max_length=100)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.investment_code
