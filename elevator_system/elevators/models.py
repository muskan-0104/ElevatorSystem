from django.db import models

# Create your models here.
class Elevator(models.Model):
    is_operational = models.BooleanField(default=True)
    is_busy = models.BooleanField(default=False)
    current_floor = models.IntegerField(default=1)
    direction = models.CharField(max_length=5, default='UP')