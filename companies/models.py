from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=30)
    logo = models.ImageField(upload_to="logos/")
