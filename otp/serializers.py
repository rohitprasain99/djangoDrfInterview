from rest_framework import serializers
from django.utils.timezone import now
from .models import Otp
from users.models import Users
from django.contrib.auth.hashers import make_password

class OtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = ['id','otp','email','expires_at']
        read_only_fields = ['id', 'expires_at'] 
    

class VerifyOtpSerializer(serializers.Serializer):
    otp=  serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self,data):
        try:
            otp_record = Otp.objects.get(otp=data['otp'])
            otp_email = otp_record.email
            otp_expires_at = otp_record.expires_at

            if not otp_email and otp_expires_at:
                raise serializers.ValidationError("Not a valid OTP")
            
            if otp_expires_at < now():
                raise serializers.ValidationError("The OTP has expired.")
            
            user = Users.objects.get(email=otp_email)
            if not user:
                raise serializers.ValidationError("Not a valid OTP")
            
            #hash new password and save user
            hashed_password = make_password(data['new_password'])
            user.set_password(hashed_password)
            user.save()

            #delete OTP
            otp_record.delete()

        except serializers.ValidationError as e:
            raise serializers.ValidationError(e.messages) 
        
        return data

