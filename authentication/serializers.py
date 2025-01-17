
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from users.models import Users 

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError("Both email and password are required.")

        user = is_authenticated(email, password)

        if not user:
            raise serializers.ValidationError("Invalid email or password.")

        data['user'] = user
        return data
    
    def create_tokens(self, user):
        user = Users.objects.get(email=user.email)
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

# utility function to check if user is authenticated
def is_authenticated(email, password):
    try:
        user = Users.objects.get(email=email)
    
        if check_password(password, user.password):
            return user
        
        return None
    
    except Users.DoesNotExist:
        return None


'''
When to Use ModelSerializer:
    - You have a Django model that you want to serialize and either create or update instances.
    - You want automatic handling for model validation, field definitions, and save operations.
    - You need to avoid repeating code and want a quick and simple approach for CRUD operations.

When to Use Serializer:
    - You are working with non-model data, like form data, data from external APIs, or any kind of custom data that does not map directly to a Django model.
    - You need to implement custom validation and custom field definitions.
    - You want more flexibility and control over the serialization process.
'''