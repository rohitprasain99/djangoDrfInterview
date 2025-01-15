from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from users.serializer import UsersSerializer  

@api_view(['POST'])
def register_user(request):

    serializer = UsersSerializer(data = request.data)

    if not serializer.is_valid():
        return Response({"message":"error while registration", "errors" : serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    serializer.save()
    return Response({"data" : {
        "email": serializer.data['email']
    }, "message"  : "user registered successfully"}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def login_user(request):
    return Response({"message": "user logged in successfully"})

@api_view(['GET'])
def user_profile(request):
    return Response({"message": "user profile returned"})

