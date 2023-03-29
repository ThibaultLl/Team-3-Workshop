from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    def __plural__(self):
        return 'Companies'