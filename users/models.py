from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser


#TODO
# user_roles = (('ADMIN','ADMIN'),('USER','USER'))
class Users(AbstractUser):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=500)
    refresh_token = models.CharField(max_length=500, default="")

    #TODO
    # role = models.CharField(max_length=500, choices = user_roles)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Add this line to specify REQUIRED_FIELDS
    REQUIRED_FIELDS = []  # If no other required fields, leave it as empty list

    USERNAME_FIELD = 'email'