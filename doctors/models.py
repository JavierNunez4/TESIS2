from django.db import models

# Create your models here.
class Kinesiologist(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    email = models.EmailField(max_length=60)
    phone_number = models.CharField(max_length=10)
    box = models.CharField(max_length=10)
    image_url = models.CharField(max_length=100)

    def __str__(self):
        return self.name