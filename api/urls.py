from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', get_status),
    path('register/', RegistrationView.as_view()),
    path('login/', obtain_auth_token),
    path('patient/', PatientView.as_view()),
    path('patient/<str:pk>/', PatientView.as_view()),
]
