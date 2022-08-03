from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', get_status),
    path('api/v1/auth/register/', RegistrationView.as_view()),
    path('api/v1/auth/login/', obtain_auth_token),
    path('api/v1/get-user/', AccountView.as_view()),
    path('api/v1/patient/', PatientView.as_view()),
    path('api/v1/patient/<str:pk>/', getPatient),
    path('api/v1/update/patient/<str:pk>/', updatePatient),
    path('api/v1/delete/patient/<str:pk>/', deletePatient),
]
