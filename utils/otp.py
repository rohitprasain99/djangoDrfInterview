from django.utils.timezone import now
from datetime import timedelta

import random
def generate_otp(expiry_minute):
    otp =  str(random.randint(100000,999999))
    expiration_time = now() + timedelta(minutes=expiry_minute)  

    return {
        'otp_code': otp,
        'expires_at' : expiration_time
    }

def is_valid_otp(otp_expires_at, expiry_minute):
    if otp_expires_at + timedelta(minutes=expiry_minute)  < now():
        return False
    return True