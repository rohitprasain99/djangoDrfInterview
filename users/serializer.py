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
