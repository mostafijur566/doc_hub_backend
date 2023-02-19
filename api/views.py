from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from .serializers import *
from rest_framework.authtoken.models import Token


# Create your views here.

@api_view(['GET'])
def get_status(request):
    return Response(
        {
            "status": 200,
            "message": "yes! django is working!"
        }
    )


class AccountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = Account.objects.get(username=request.user)
        serializer = RegistrationSerializers(user, many=False)

        return Response(
            {
                "name": serializer.data['name'],
                "email": serializer.data['email'],
                "username": serializer.data['username']
            }
        )


class RegistrationView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = RegistrationSerializers(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['message'] = "Successfully registered"
            data['name'] = account.name
            data['email'] = account.email
            data['username'] = account.email
            data['username'] = account.username
            token = Token.objects.get(user=account).key
            data['token'] = token

        else:
            data = {
                "status": 400,
                "message": "something went wrong",
                "data": serializer.errors
            }

        return Response(data)

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = Account
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data.get("old_password")
            new_password = serializer.data.get("new_password")
            confirm_new_password = serializer.data.get("confirm_new_password")

            if not self.object.check_password(old_password):
                return Response({
                    "message": "Wrong password"
                }, status=status.HTTP_400_BAD_REQUEST)

            if new_password != confirm_new_password:
                return Response({
                    "message": "New password do not match"}, status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(new_password)
            self.object.save()
            update_session_auth_hash(request, self.object)  # Important!
            return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PatientView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PatientSerializers(data=request.data)

        if serializer.is_valid():
            serializer.save()
            data = {
                "message": "Patient details added successfully",
                "data": serializer.data
            }

        else:
            data = {
                "status": 400,
                "message": serializer.errors,
            }

        return Response(data)

    def get(self, request):
        patients = PatientDetails.objects.filter(doctor_id=request.user)
        serializer = PatientSerializers(patients, many=True)

        return Response(
            {
                "total_patients": PatientDetails.objects.count(),
                "patients": serializer.data
            }
        )


class PatientSearchView(ListAPIView):
    queryset = PatientDetails.objects.all()
    serializer_class = PatientSerializers
    filter_backends = [SearchFilter]
    search_fields = [
        'name',
        'age',
        'weight',
        'gender',
        'medicine',
        'disease',
    ]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Filter by doctor_id
        queryset = queryset.filter(doctor_id=request.user)

        serializer = self.get_serializer(queryset, many=True)
        data = {
            "total_patients": len(serializer.data),
            "patients": serializer.data,
        }
        return Response(data)

@api_view(['GET'])
def getPatient(request, pk):
    patient = PatientDetails.objects.get(id=pk)
    serializer = PatientSerializers(patient, many=False)

    return Response(serializer.data)


@api_view(['PUT'])
def updatePatient(request, pk):
    patient = PatientDetails.objects.get(id=pk)
    serializer = PatientSerializers(patient, data=request.data)

    if serializer.is_valid():
        serializer.save()
        data = {
            "message": "Updated successfully!"
        }

    else:
        data = {
            "message": 400
        }

    return Response(data)


@api_view(['DELETE'])
def deletePatient(request, pk):
    patient = PatientDetails.objects.get(id=pk)
    patient.delete()

    return Response(
        {
            "message": "Patient data deleted!"
        }
    )
