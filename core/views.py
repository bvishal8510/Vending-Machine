from django.shortcuts import render, redirect, reverse
from django.views import generic, View
from django.http import HttpResponse, JsonResponse
from core.models import VendingItems, VendingMachineMoney, UserMoney


class DisplayVendingMachine(View):
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


class SaveValue(View):

    def get(self, request):
        num = request.GET['num']
        user_money = list(UserMoney.objects.all())[0]
        pk=user_money.pk
        penny_count = user_money.u_penny
        nickel_count = user_money.u_nickel
        dime_count = user_money.u_dime
        quater_count = user_money.u_quater
        if(int(num)==1):
            penny_count += 1
        elif(int(num)==5):
            nickel_count += 1
        elif(int(num)==10):
            dime_count += 1
        else:
            quater_count += 1
        UserMoney.objects.filter(pk=pk).update(u_penny=penny_count, u_nickel=nickel_count, u_dime=dime_count, u_quater=quater_count)
        return JsonResponse({})

class CommitTransaction(View):
    
    def get(self, request, price, *args, **kwargs):
        print(price)
        vending_machine_data = VendingItems.objects.get(pk=1)
        # return render(self.request, self.template_name, {"data":vending_machine_data})


class CancelTransaction(View):
    
    def get(self, request, price, *args, **kwargs):
        UserMoney.objects.all().delete()
        # vending_machine_data = VendingItems.objects.get(pk=1)
        # return render(self.request, self.template_name, {"data":vending_machine_data})