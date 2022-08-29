from django.db import models

import sys
sys.path.append('../')

from Users.models import Member

class Sport(models.Model):
    name = models.CharField(max_length=50,primary_key=True)

class Slot(models.Model):
    slot = models.CharField(max_length=50,primary_key=True)
    
class SportSpecificSlot(models.Model):
    name = models.ForeignKey(Sport, on_delete=models.CASCADE)
    court = models.CharField(max_length=50)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    available = models.BooleanField()

class Booking(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    court = models.CharField(max_length=50)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)