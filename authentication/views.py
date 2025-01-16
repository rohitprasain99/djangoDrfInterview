from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken
from users.serializer import UsersSerializer, LoginSerializer  

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
    try:
        refresh_token = request.data.get("refresh")
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Token successfully blacklisted"}, status=200)
    except Exception as e:
            return Response({"error": str(e)}, status=400)
