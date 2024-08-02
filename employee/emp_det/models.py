from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Address(models.Model):
    add_line = models.CharField(max_length=255, blank=True, null=False)
    state = models.CharField(max_length=100, blank=True, null=False)
    hometown = models.CharField(max_length=100, blank=True, null=False)
    pincode = models.CharField(max_length=6, blank=True, null=False)

    def __str__(self):
        return f"{self.add_line}, {self.hometown}, {self.state}, {self.pincode}"

class Employee(models.Model):
    name = models.CharField(max_length=240, unique=True, null=False, blank=True)
    phone = models.JSONField(default=list, null=False, blank=True)

    company = models.TextField(max_length=240, null=False, blank=True)
    role = models.CharField(max_length=240, null=False, blank=True)
    active = models.BooleanField(default=True, null=False, blank=True)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=False, blank=True, default=1)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if self.address:
            self.address.delete()
        super().delete(*args, **kwargs)

class Project(models.Model):
    STATUS_CHOICES = (
        ('Ongoing', 'Ongoing'),
        ('Done', 'Done'),
    )
    
    title = models.CharField(max_length=240, unique=True, null=False, blank=True)
    description = models.TextField(max_length=240, null=False, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    duration = models.IntegerField(default=0, null=False, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='projects', null=False, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Ongoing', null=False, blank=True)

    def save(self, *args, **kwargs):
        if self.start_date and self.end_date:
            self.duration = (self.end_date - self.start_date).days
            if self.duration < 0:
                raise ValidationError("End date must be after the start date.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
