from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import UserDetailSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import UserDetail

@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def get_user_profile(request):
    try:
        user_id = request.user.id
        
        user_detail = UserDetail.objects.get(user_id= user_id)

        if not user_detail:
             raise Exception("User profile not found")
        
        serializer = UserDetailSerializer(user_detail)
        
        return Response({"data": {
            "first_name": serializer.data['first_name'],
            "last_name": serializer.data['last_name'],
            "country": serializer.data['country'],
            "contact": serializer.data['contact'],
            "email" : serializer.data['user_info']['email']
        }, "message": "User profile updated successfully"}, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def create_user_profile(request):
    try:
        user = request.user
        data = request.data
        data['user'] = user.id

        serializer = UserDetailSerializer(data = data)

        if not serializer.is_valid():
            return Response({"message":"Error creating profile", "errors" : serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response({"data": {
            "first_name": serializer.data['first_name'],
            "last_name": serializer.data['last_name'],
            "country": serializer.data['country'],
            "contact": serializer.data['contact'],
        }, "message": "User created successfully"}, status=status.HTTP_201_CREATED)
    
    except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated]) 
def update_user_profile(request):
    try:
        user_id = request.user.id
        user_detail = UserDetail.objects.get(user_id= user_id) 
        if not user_detail:
             raise Exception("User profile not found")
        
        ''' Create a serializer with the existing instance, 
            passing partial=True for partial updates
        '''
        serializer = UserDetailSerializer(user_detail, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response({"message":"Error creating profile", "errors" : serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response({"data": {
            "first_name": serializer.data['first_name'],
            "last_name": serializer.data['last_name'],
            "country": serializer.data['country'],
            "contact": serializer.data['contact'],
            "email" : serializer.data['user_info']['email']
        }, "message": "User profile updated successfully"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated]) 
def delete_user_profile(request):
    try:
        user_id = request.user.id
        user_detail = UserDetail.objects.get(user_id= user_id)
    
        if not user_detail:
            raise Exception("UserDetail not found.")
        
        user_detail.delete() 
        return Response({ "message"  : "User detail deleted successfully"}, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
  