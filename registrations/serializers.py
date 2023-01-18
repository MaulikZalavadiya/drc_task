from django.contrib.auth.password_validation import validate_password

from rest_framework.serializers import ModelSerializer, Serializer

from phonenumber_field.serializerfields import PhoneNumberField

from custom_auth.models import User


class CheckPhoneSerializer(Serializer):
    phone = PhoneNumberField(required=True)


class CheckUserDataSerializer(ModelSerializer):
    phone = PhoneNumberField()

    class Meta:
        model = User
        fields = ('email', 'username', 'contact', 'password')


class RegistrationSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('email','username', 'contact', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)

        # password assigment
        user.set_password(password)
        user.save(update_fields=['password'])

        return user
