from django.db import models
from doctors.models import Kinesiologist
# Create your models here.
class Availability(models.Model):
    DAYS = [
        (0, 'Lunes'),
        (1, 'Martes'),
        (2, 'Miércoles'),
        (3, 'Jueves'),
        (4, 'Viernes'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]

    kinesiologist = models.ForeignKey(Kinesiologist, on_delete=models.CASCADE, related_name="availability")
    day = models.IntegerField(choices=DAYS)
    start_time = models.TimeField()  # Ej: 08:00
    end_time = models.TimeField()    # Ej: 12:00

    def __str__(self):
        return f"{self.kinesiologist} - {self.get_day_display()} {self.start_time} - {self.end_time}"