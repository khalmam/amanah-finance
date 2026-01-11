from django.contrib import admin
from .models import BusinessProposal

@admin.register(BusinessProposal)
class BusinessProposalAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'status',
        'approved_by',
        'approved_at',
        'created_at'
    )
    list_filter = ('status',)
    readonly_fields = ('approved_by', 'approved_at')
