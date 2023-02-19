from rest_framework import serializers
from .models import *


class AccountSerializers(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['name', 'email', 'username']


class RegistrationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['name', 'email', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        account = Account(
            name=self.validated_data['name'],
            email=self.validated_data['email'],
            username=self.validated_data['username']
        )

        password = self.validated_data['password']
        account.set_password(password)
        account.save()
        return account


class PatientSerializers(serializers.ModelSerializer):
    class Meta:
        model = PatientDetails
        fields = '__all__'

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)
