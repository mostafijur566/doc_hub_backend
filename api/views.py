from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
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
        patients = PatientDetails.objects.all()
        serializer = PatientSerializers(patients, many=True)

        return Response(
            {
                "total_patients": PatientDetails.objects.count(),
                "patients": serializer.data
            }
        )

    def put(self, request, pk):
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

        return Response(serializer.data)

    def delete(self, request, pk):
        patient = PatientDetails.objects.get(id=pk)
        patient.delete()

        return Response(
            {
                "message": "Patient data deleted!"
            }
        )

@api_view(['GET'])
def getPatient(request, pk):
    patient = PatientDetails.objects.get(id=pk)
    serializer = PatientSerializers(patient, many=False)

    return Response(
        {
            "total_patients": PatientDetails.objects.count(),
            "patients": serializer.data
        }
    )
