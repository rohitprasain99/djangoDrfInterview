from django.db import models
from django.utils.timezone import now
import uuid
class Otp(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)

    otp = models.CharField(max_length=500)
    email = models.EmailField(max_length=254, unique=True)

    expires_at = models.DateTimeField(auto_now_add=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_valid(self):
        return now() < self.expires_at