from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from doctors.models import Kinesiologist
from .models import Appointment, Availability
from .serializers import (
    AppointmentSerializer,
    AvailabilitySerializer,
    KinesiologistSummarySerializer,
)


class AvailabilityListCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, kinesiologist_id: int):
        kinesiologist = get_object_or_404(Kinesiologist.objects.select_related('user'), pk=kinesiologist_id)

        availability_qs = (
            Availability.objects.filter(kinesiologist=kinesiologist)
            .order_by('day', 'start_time')
        )
        appointments_qs = (
            Appointment.objects.filter(kinesiologist=kinesiologist)
            .select_related('patient_name__user', 'kinesiologist__user')
            .order_by('date', 'start_time')
        )

        availability = AvailabilitySerializer(availability_qs, many=True)
        appointments = AppointmentSerializer(appointments_qs, many=True)
        kinesiologist_data = KinesiologistSummarySerializer(kinesiologist)

        return Response(
            {
                "kinesiologist": kinesiologist_data.data,
                "availability": availability.data,
                "appointments": appointments.data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request, kinesiologist_id: int):
        kinesiologist = get_object_or_404(Kinesiologist.objects.select_related('user'), pk=kinesiologist_id)

        if not (
            request.user.is_superuser
            or request.user == kinesiologist.user
        ):
            return Response(
                {
                    "status": False,
                    "message": "No tiene permisos para registrar este horario.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = AvailabilitySerializer(
            data=request.data,
            context={'kinesiologist': kinesiologist},
        )
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                availability = serializer.save(kinesiologist=kinesiologist)
        except ValidationError as exc:
            message = getattr(exc, 'message', None) or getattr(exc, 'messages', [str(exc)])[0]
            return Response(
                {
                    "status": False,
                    "message": message,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except IntegrityError:
            return Response(
                {
                    "status": False,
                    "message": "No fue posible guardar el horario. Intente nuevamente.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {
                "status": True,
                "message": "Horario registrado correctamente.",
                "availability": AvailabilitySerializer(availability).data,
            },
            status=status.HTTP_201_CREATED,
        )


class AppointmentCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, kinesiologist_id: int):
        kinesiologist = get_object_or_404(Kinesiologist.objects.select_related('user'), pk=kinesiologist_id)

        serializer = AppointmentSerializer(
            data=request.data,
            context={'kinesiologist': kinesiologist},
        )
        serializer.is_valid(raise_exception=True)

        patient = serializer.validated_data['patient_name']
        is_authorized = request.user.is_superuser or request.user == patient.user or request.user == kinesiologist.user
        if not is_authorized:
            return Response(
                {
                    "status": False,
                    "message": "No tiene permisos para agendar esta hora médica.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            with transaction.atomic():
                appointment = serializer.save()
        except ValidationError as exc:
            message = getattr(exc, 'message', None) or getattr(exc, 'messages', [str(exc)])[0]
            return Response(
                {
                    "status": False,
                    "message": message,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except IntegrityError:
            return Response(
                {
                    "status": False,
                    "message": "No fue posible agendar la hora médica. Intente nuevamente.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        appointment_data = AppointmentSerializer(appointment).data
        return Response(
            {
                "status": True,
                "message": "Hora médica reservada correctamente.",
                "appointment": appointment_data,
            },
            status=status.HTTP_201_CREATED,
        )
