from rest_framework import serializers
from .models import UserDetail
from users.serializers import UsersSerializer
from users.models import Users
class UserDetailSerializer(serializers.ModelSerializer):
    # Nested user info for read operations
    user_info = UsersSerializer(source='user', read_only=True)

    # Foreign key for write operations
    user = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all(), write_only=True)

    class Meta:
        model = UserDetail
        # fields = '__all__'
        fields = ['id', 'first_name', 'last_name','country','contact','user', 'user_info']
