from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def user_profile(request):
    return Response({
                'data': "ok"
        }) 
    try:
        serializer = LoginSerializer(data = request.user)

        if  not serializer.is_valid():
            return Response({
                "message" : "user unauthorized",
                "errors" : serializer.errors
            }, status = status.HTTP_401_UNAUTHORIZED)
        
        return Response({
                'data': serializer.email
        })
    except Exception as e:
        return Response({
            "errors" : e
        }, status = status.HTTP_400_BAD_REQUEST)