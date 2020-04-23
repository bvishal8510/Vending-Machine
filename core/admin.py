from django.contrib import admin
from core.models import VendingItems, VendingMachineMoney, UserMoney
# Register your models here.


admin.site.register(VendingItems)
admin.site.register(VendingMachineMoney)
admin.site.register(UserMoney)
