from django.db import models
from users.models import Users
import uuid

class UserDetail(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=500)
    last_name = models.CharField(max_length=500)
    country = models.CharField(max_length=500)
    contact = models.CharField(max_length=500)
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name="detail")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


