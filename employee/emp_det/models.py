from django.db import models
from django.core.exceptions import ValidationError
import re

# Create your models here.
class Address(models.Model):
    add_line = models.CharField(max_length=255)
    state = models.CharField(max_length=100)
    hometown = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)

    def __str__(self):
        return f"{self.add_line}, {self.hometown}, {self.state}, {self.pincode}"

class Employee(models.Model):
    name = models.CharField(max_length=240, unique=True)
    phone = models.JSONField(default=list)

    company = models.TextField(max_length=240)
    role = models.CharField(max_length=240)
    active = models.BooleanField(default=True)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.name

class Project(models.Model):
    STATUS_CHOICES = (
        ('Ongoing', 'Ongoing'),
        ('Done', 'Done'),
    )
    
    title = models.CharField(max_length=240, unique=True)
    description = models.TextField(max_length=240)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    duration = models.IntegerField(default=0)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='projects')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Ongoing')

    def save(self, *args, **kwargs):
        if self.start_date and self.end_date:
            self.duration = (self.end_date - self.start_date).days
            if self.duration < 0:
                raise ValidationError("End date must be after the start date.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
