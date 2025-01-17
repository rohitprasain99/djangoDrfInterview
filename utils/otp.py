from django.utils.timezone import now
import random
def generate_otp():
    otp =  random.randint(100000,999999)
    return otp

def is_valid_otp():
    pass