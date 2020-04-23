from .models import VendingMachineMoney

def reset_function(modeladmin, request, queryset):
    pk = (list(queryset)[0]).pk
    VendingMachineMoney.objects.filter(pk=pk).update(m_penny=0, m_nickel=0, m_dime=0, m_quater=0)

