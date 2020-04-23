from django.contrib import admin
from core.models import VendingItems, VendingMachineMoney, UserMoney
from core.reset import reset_function
# Register your models here.

class ResetAdmin(admin.ModelAdmin):
    actions = [reset_function]

    class Meta:
        model = VendingMachineMoney


admin.site.register(VendingItems)
admin.site.register(VendingMachineMoney, ResetAdmin)
admin.site.register(UserMoney)
