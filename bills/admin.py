from django.contrib import admin
from .models import Bill, Legislator, Vote, VoteResult


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    """
    This ModelAdmin configures the admin interface for the Bill model.
    """


@admin.register(Legislator)
class LegislatorAdmin(admin.ModelAdmin):
    """
    This ModelAdmin configures the admin interface for the Legislator model.
    """


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    """
    This ModelAdmin configures the admin interface for the Vote model.
    """


@admin.register(VoteResult)
class VoteResultAdmin(admin.ModelAdmin):
    """
    This ModelAdmin configures the admin interface for the VoteResult model.
    """
