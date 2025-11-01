from django.shortcuts import render
from django.utils.decorators import method_decorator
import json 
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import Doctors
# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
class DoctorListView(View):
    def get(self, request):
        if Doctors.objects.values().acount() != 0:
            doctors = list(Doctors.objects.values())
            return JsonResponse(doctors, safe=False)
        else:
            return JsonResponse({"status":True, "msg":"List Is Empty"})
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            doctor = Doctors.objects.create(
                name = data["name"],
                specialty = data["specialty"],
                schedule = data.get("horario","")
            )
            return JsonResponse({"id":doctor.id, "nombre":doctor.name}, status=201)
        except Exception as e:
            return JsonResponse({"stauts":False, "error": str(e)}, status=400)