from django.contrib import admin
from core.models import Contract, Rate


class ContractAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')


class RateAdmin(admin.ModelAdmin):
    list_display = ('origin', 'destination', 'currency',
                    'twenty', 'forty', 'fortyhc', 'contract')


admin.site.register(Contract, ContractAdmin)
admin.site.register(Rate, RateAdmin)
