from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status

from .models import Kinesiologist 
from .serializers import KinesiologistSerializer

class kinesiologistListCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print("USER:", request.user)
        print("AUTH:", request.auth)
        kinesiologist = Kinesiologist.objects.all()
        serializer = KinesiologistSerializer(kinesiologist, many=True)
        return Response(serializer.data)
    
    def post (self, request):
        print("USER:", request.user)
        print("AUTH:", request.auth)
        if not request.user.is_superuser:
            return Response({"status":False, "message":"No Autorizado"}, status=403)
        
        serializer = KinesiologistSerializer(data=request.data)

        if serializer.is_valid():
            kine = serializer.save(user=request.user)
            return Response({
                            "status": True,
                            "user": {
                                "id": kine.id,
                                "name": kine.name,
                                "rut": kine.rut,
                                "email":kine.user.email,
                                "specialty": kine.specialty,
                                "phone_number": kine.phone_number,
                                "box": kine.box,
                                "image_url": kine.image_url
                            }
                        })
        
        return Response(serializer.errors, status=400)