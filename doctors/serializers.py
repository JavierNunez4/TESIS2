from rest_framework import serializers
from .models import Kinesiologist

class KinesiologistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kinesiologist
        fields = ['name', 'rut', 'specialty', 'phone_number', 'box'] 