from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from users.models import Users 

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'email', 'password', 'refresh_token']

        #read only fields are included in the response but cannot be modified or updated.
        read_only_fields = ['id', 'refresh_token'] 
        extra_kwargs = {
            'password': {'write_only': True} # not included in the response
        }

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def create(self, validated_data):
        hashed_password = make_password(validated_data['password'])

        user = Users( 
                email=validated_data.get('email'), #required field
                password = hashed_password
            )
        user.save()
        return user

