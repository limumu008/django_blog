from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.PositiveIntegerField('折扣率', validators=[MaxValueValidator(100), MinValueValidator(0)])
    is_actived = models.BooleanField()

    def __str__(self):
        return self.code
