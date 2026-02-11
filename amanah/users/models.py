from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models

# class User(AbstractUser):
#     ROLE_CHOICES = (
#         ('admin', 'Admin'),
#         ('investor', 'Investor'),
#         ('entrepreneur', 'Entrepreneur'),
#     )
#     role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    


class User(AbstractUser):
    ROLE_CHOICES = [
        ('entrepreneur', 'Entrepreneur'),
        ('moderator', 'Moderator'),
        ('investor', 'Investor'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    # Optional fields for extra info
    company_name = models.CharField(max_length=255, blank=True, null=True)
    business_sector = models.CharField(max_length=255, blank=True, null=True)
    investment_interests = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"