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


    approved_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='approved_proposals'
    )
    approved_at = models.DateTimeField(null=True, blank=True)

    is_contracted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    interested_investors = models.ManyToManyField(
        User, 
        related_name='interested_proposals',
        blank=True,
        limit_choices_to={'role': 'investor'}
    )
    
    def __str__(self):
        return self.title
