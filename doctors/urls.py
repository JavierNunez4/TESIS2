from django.urls import path
from .views import kinesiologistListCreateView

urlpatterns = [
    path('kinesiologists', kinesiologistListCreateView.as_view(), name='doctor-list'),
]
