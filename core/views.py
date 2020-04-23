from django.shortcuts import render, redirect, reverse
from django.views import generic
from core.models import VendingItems, VendingMachineMoney, UserMoney


class DisplayVendingMachine(generic.DetailView):
    template_name = 'core/vending_machine.html'

    def dispatch(self, request, *args, **kwargs):
        if list(VendingItems.objects.all()) == []:
            VendingItems.objects.create(coke_price=25, pepsi_price=35, soda_price=45, coke_quantity=0,
            pepsi_quantity=0, soda_quantity=0)
        if list(VendingMachineMoney.objects.all()) == []:
            VendingMachineMoney.objects.create(m_penny=0, m_nickel=0, m_dime=0, m_quater=0)
        if list(UserMoney.objects.all()) == []:
            UserMoney.objects.create(u_penny=0, u_nickel=0, u_dime=0, u_quater=0)

        return super(DisplayVendingMachine, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        vending_machine_data = VendingItems.objects.get(pk=1)
        return render(self.request, self.template_name, {"data":vending_machine_data})