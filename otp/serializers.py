from rest_framework import serializers
from .models import Otp
class OtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = ['id','otp','email','expires_at']
        read_only_fields = ['id', 'expirest_at'] 