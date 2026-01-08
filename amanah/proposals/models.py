from django.db import models

# Create your models here.

from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class BusinessProposal(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    entrepreneur = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='proposals'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    capital_required = models.DecimalField(max_digits=12, decimal_places=2)
    duration_months = models.PositiveIntegerField()
    investor_profit_ratio = models.PositiveIntegerField()
    entrepreneur_profit_ratio = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
