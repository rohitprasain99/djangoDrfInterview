from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password

from utils.otp import generate_otp, is_valid_otp
from users.serializers import UsersSerializer,EmailSerializer
from authentication.serializers import LoginSerializer  
from otp.serializers import OtpSerializer
from otp.models import Otp
from users.models import Users


from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import now

otp_expiration_min = 5

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
        return Response({"message":"invalid email or password", "errors":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

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
    otp = generate_otp(otp_expiration_min) 

    # save OTP and email to db
    serialized_otp = OtpSerializer(data = {
        "email":valid_email, 
        "otp":otp['otp_code'],
        "expires_at":otp['expires_at']
        })
    if not serialized_otp.is_valid():
        return Response({"errors":serialized_otp.errors}, status=status.HTTP_400_BAD_REQUEST)
    serialized_otp.save()
    
    # TODO
    # try:
    #     subject = 'Your OTP Code'
    #     message = f'Your OTP code is: {otp['otp_code']}. Please use it to reset your password.'
    #     email_from = settings.EMAIL_HOST_USER
    #     recipient_list = [email]
    #     send_mail(subject, message, email_from, recipient_list)

    # except Exception as e:
    #     return Response({"message":"Could not send email", "errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)
   
    return Response({
        "message": "please check mail for OTP code. It expires in 1 minute",
        "otp": otp['otp_code']
    },status = status.HTTP_200_OK)


@api_view(['POST'])
def new_password_otp(request):
    otp = request.data['otp']
    new_password = request.data['new_password']

    if not otp and not new_password:
        return Response({"error": "OTP and new password are required."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        otp_record = Otp.objects.get(otp = otp)
        otp_email = otp_record.email
        otp_expires_at = otp_record.expires_at
        if not otp_email and otp_expires_at:
            raise Exception("Not a valid OTP")
        
        if not is_valid_otp(otp_expires_at=otp_expires_at, expiry_minute = otp_expiration_min ):
            raise Exception("The OTP has expired.")
      
        user = Users.objects.get(email=otp_email)
        if not user:
            raise Exception("Not a valid OTP")
        
        #hash new password and save user, 
        #set_password already hashes the password string, not need to hash again
        user.set_password(new_password)
        user.save()

        #delete OTP
        otp_record.delete()

        return Response({
            "message": "Password changed successfully"
        }, status= status.HTTP_200_OK)

    except Exception as e:
        return Response({"message":"Could not change password", "errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def change_password(request):
    # print(request.user.password)
    try:
        user = request.user
        current_password = request.data['current_password']
        new_password = request.data['new_password']

        if not current_password:
            return Response({"message":"Current password required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not new_password:
            return Response({"message":"New password required"}, status=status.HTTP_400_BAD_REQUEST)
        
        #check the current password with password from db
        is_valid_password = check_password(current_password, user.password)
        if not is_valid_password:
            return Response({"message":"Incorrect current password"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({
            'message': "Password updated successfully",
        },status=status.HTTP_200_OK) 
    
    except Exception as e:
        return Response({"message":"Could not change password", "errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)  