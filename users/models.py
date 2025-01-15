from django.db import models
import uuid

#TODO
# user_roles = (('ADMIN','ADMIN'),('USER','USER'))
class Users(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=500)
    refresh_token = models.CharField(max_length=500, default="")

    #TODO
    # role = models.CharField(max_length=500, choices = user_roles)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)