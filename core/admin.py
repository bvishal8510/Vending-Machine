from django.contrib import admin
from core.models import VendingItems, VendingMachineMoney, UserMoney, VendingItemsNew
from core.reset import reset_function
# Register your models here.

class ResetAdmin(admin.ModelAdmin):          #implements reset feature in admin
    actions = [reset_function]

    class Meta:
        model = VendingMachineMoney


admin.site.register(VendingItems)
admin.site.register(VendingMachineMoney, ResetAdmin)
admin.site.register(UserMoney)
admin.site.register(VendingItemsNew)
