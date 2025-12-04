from django.urls import path

from .views import AppointmentCreateView, AvailabilityListCreateView

urlpatterns = [
    path('kinesiologists/<int:kinesiologist_id>/availability',AvailabilityListCreateView.as_view(), name='kinesiologist-availability',),
    path('kinesiologists/<int:kinesiologist_id>/appointments',AppointmentCreateView.as_view(),name='kinesiologist-appointments',),
]
