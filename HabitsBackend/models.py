from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username
    
    
class Counter(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="counters")
    counterTitle = models.CharField(max_length=255)
    createdOn = models.DateField(default=date.today)
    value = models.IntegerField(default=0)
    updatedAt = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.counterTitle} ({self.value})"
    
    
class Reward(models.Model):
    counter = models.ForeignKey(Counter, on_delete=models.CASCADE, related_name="validRewards")
    title = models.CharField(max_length=255)
    trigger = models.IntegerField()

    def __str__(self):
        return f"{self.title} trig: {self.trigger}"