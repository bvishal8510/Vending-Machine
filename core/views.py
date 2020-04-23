from django.shortcuts import render, redirect, reverse
from django.views import generic, View
from django.http import HttpResponse, JsonResponse
from core.models import VendingItems, VendingMachineMoney, UserMoney
from django.contrib import messages
from django.urls import reverse_lazy


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


class CancelTransaction(View):
    
    def get(self, request, *args, **kwargs):
        user_money = list(UserMoney.objects.all())[0]
        to_message = "Transaction cancelled! Here is your "+str(user_money.u_penny)+" penny, "+str(user_money.u_nickel)+" nickel, "+\
                        str(user_money.u_dime)+" dime, "+str(user_money.u_quater)+" quater"
        messages.add_message(request, messages.INFO, to_message)
        UserMoney.objects.all().delete()
        return redirect(reverse_lazy('display_machine'))


class CommitTransaction(View):
    
    def get(self, request, price, *args, **kwargs):
        vending_machine_data = VendingItems.objects.get(pk=1)
        user_money = list(UserMoney.objects.all())[0]
        vending_machine_money = list(VendingMachineMoney.objects.all())[0]
        vending_money_pk=vending_machine_money.pk
        vending_machine_data_pk = vending_machine_data.pk

        if(((price == vending_machine_data.coke_price) and (vending_machine_data.coke_quantity == 0)) or\
            ((price == vending_machine_data.pepsi_price) and (vending_machine_data.pepsi_quantity == 0)) or\
            ((price == vending_machine_data.soda_price) and (vending_machine_data.soda_quantity == 0))):
            to_message = "Transaction cancelled! Out of Stock. Here is your "+str(user_money.u_penny)+" penny, "+ \
                str(user_money.u_nickel)+" nickel, "+ \
                str(user_money.u_dime)+" dime, "+str(user_money.u_quater)+" quater"
            messages.add_message(request, messages.INFO, to_message)
            UserMoney.objects.all().delete()
            return redirect(reverse_lazy('display_machine'))                        
        total_money = 1*user_money.u_penny + 5*user_money.u_nickel + 10*user_money.u_dime + 25*user_money.u_quater        
        change = total_money - price        
        quater_change = int(change/25) if int(change/25)<(vending_machine_money.m_quater + user_money.u_quater)\
                                         else (vending_machine_money.m_quater + user_money.u_quater)
        change = change - (25*quater_change)        
        dime_change = int(change/10) if int(change/10)<(vending_machine_money.m_dime + user_money.u_dime)\
                                     else (vending_machine_money.m_dime + user_money.u_dime)
        change = change - (10*dime_change)        
        nickel_change = int(change/5) if int(change/5)<(vending_machine_money.m_nickel + user_money.u_nickel)\
                                         else (vending_machine_money.m_nickel + user_money.u_nickel)
        change = change - (5*nickel_change)        
        penny_change = change if change<(vending_machine_money.m_penny + user_money.u_penny)\
                                else (vending_machine_money.m_penny + user_money.u_penny)
        change = change - penny_change        

        if(change != 0):
            to_message = "Transaction cancelled! No change found. Here is your "+str(user_money.u_penny)+" penny, "+ \
                str(user_money.u_nickel)+" nickel, "+ \
                str(user_money.u_dime)+" dime, "+str(user_money.u_quater)+" quater"
            messages.add_message(request, messages.INFO, to_message)
            UserMoney.objects.all().delete()
            return redirect(reverse_lazy('display_machine'))

        else:
            VendingMachineMoney.objects.filter(pk=vending_money_pk).update( m_penny=vending_machine_money.m_penny + user_money.u_penny - penny_change,
                                                              m_nickel=vending_machine_money.m_nickel + user_money.u_nickel - nickel_change,
                                                              m_dime=vending_machine_money.m_dime + user_money.u_dime - dime_change,
                                                              m_quater=vending_machine_money.m_quater + user_money.u_quater - quater_change)
            if(price==vending_machine_data.coke_price):
                to_message = "Coke Pops Out!"
                coke = vending_machine_data.coke_quantity - 1
                VendingItems.objects.filter(pk=vending_machine_data_pk).update(coke_quantity=coke)
            elif(price==vending_machine_data.pepsi_price):
                to_message = "Pepsi Pops Out!"
                pepsi = vending_machine_data.pepsi_quantity - 1
                VendingItems.objects.filter(pk=vending_machine_data_pk).update(pepsi_quantity=pepsi)
            else:
                to_message = "Soda Pops Out! "
                soda = vending_machine_data.soda_quantity - 1
                VendingItems.objects.filter(pk=vending_machine_data_pk).update(soda_quantity=soda)
            to_message += "Here is your " + str(penny_change) + " penny, " + \
                            str(nickel_change) + " nickel, " + \
                            str(dime_change)+" dime, " + str(quater_change) + " quater"
            messages.add_message(request, messages.INFO, to_message)
            UserMoney.objects.all().delete()
            return redirect(reverse_lazy('display_machine'))

