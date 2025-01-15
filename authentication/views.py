from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def register_user(request):
    return Response({"message": "user registered successfully"})

@api_view(['GET'])
def login_user(request):
    return Response({"message": "user logged in successfully"})

@api_view(['GET'])
def user_profile(request):
    return Response({"message": "user profile returned"})

