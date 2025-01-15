from django.db import models

class Users(models.Model):
    id = models.UUIDField(primary_key=True)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=500)
    refresh_token = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # class Meta:
    #     abstract = True

'''
abstract = True
- tells Django that TimeStampedModel is an abstract model
- which means it won\’t create a separate table for this class
- but the fields will be added to any models that inherit from it.
'''