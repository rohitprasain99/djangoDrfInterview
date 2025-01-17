from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


from users.serializers import UsersSerializer,EmailSerializer
from authentication.serializers import LoginSerializer  
from utils.otp import generate_otp
@api_view(['POST'])
def register_user(request):

    serializer = UsersSerializer(data = request.data)

    if not serializer.is_valid():
        return Response({"message":"error while registration", "errors" : serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    serializer.save()
    return Response({"data" : {
        "email": serializer.data['email']
    }, "message"  : "user registered successfully"}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login_user(request):
    
    serializer = LoginSerializer(data=request.data)
    
    if not serializer.is_valid():
        print(serializer.errors)
        return Response({"message":"invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)

    # print(">>>>>>>>>", serializer.validated_data)
    user = serializer.validated_data['user']
    tokens = serializer.create_tokens(user)

    return Response({"data" : {
        "access_token": tokens['access'],
        "refresh_token": tokens['refresh'],
        "message" : "logged in successfully"}},
     status=status.HTTP_200_OK)


@api_view(['POST'])
def logout(request):
    refresh_token = request.data.get('refresh_token')

    if not refresh_token:
        return Response({'detail': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        refresh_token = request.data.get("refresh_token")
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Token successfully blacklisted"}, status=status.HTTP_200_OK)
    except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def generate_new_access_token(request):

    refresh_token = request.data.get('refresh_token')

    if not refresh_token:
        return Response({'detail': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        refresh = RefreshToken(refresh_token)
        return Response({
            'access_token': str(refresh.access_token)
        })

    except Exception as e:
        return Response({'detail': 'Invalid or expired refresh token.'}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def forget_password(request):
    email = request.data.get('email')

    if not email:
        return Response({
            "message":"email is required"
        })
    

    # check if email is correct
    serialized_email = EmailSerializer(data = {"email":email})  # always accept dictionary

    if not serialized_email.is_valid():
            return Response({"errors":serialized_email.errors}, status=status.HTTP_400_BAD_REQUEST)

    valid_email = serialized_email.validated_data['email']

    #set expiration time (e.g., 5 minutes)
    otp = generate_otp(5) 

        
    return Response({
        "message": "please check mail for OTP code",
        "email"  : valid_email,
        "otp": otp
    },status = status.HTTP_200_OK)


@api_view(['POST'])
def change_password(request):
    pass


