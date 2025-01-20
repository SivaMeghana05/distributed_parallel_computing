from django.db import models

class Aircraft(models.Model):
    registration = models.CharField(max_length=10, unique=True)
    model = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=50)
    year_manufactured = models.IntegerField()
    capacity = models.IntegerField()
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('maintenance', 'In Maintenance'),
        ('retired', 'Retired')
    ])

    def __str__(self):
        return f"{self.registration} - {self.model}" 