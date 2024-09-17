from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    CLIENT_TYPES = [
        ('Simple', 'Simple'),
        ('Professional', 'Professional'),
        ('Business', 'Business'),
    ]

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(null=True, max_length=255)
    company_name = models.CharField(null=True, max_length=255)
    designation = models.CharField(null=True, max_length=255)
    contact_info = models.TextField(null=True)
    email = models.EmailField(null=True)
    phone_number = models.CharField(null=True, max_length=15)
    address = models.TextField(null=True)
    industry = models.CharField(max_length=255, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    client_type = models.CharField(max_length=20, choices=CLIENT_TYPES, default='Simple')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
