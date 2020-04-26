from django.shortcuts import render, redirect, reverse
from django.views import generic, View
from django.http import HttpResponse, JsonResponse
from core.models import VendingItems, VendingMachineMoney, UserMoney, VendingItemsNew
from django.contrib import messages
from django.urls import reverse_lazy


class DisplayVendingMachine(View):                   #displays vending machine and various messages of Completion and failure
    template_name = 'core/vending_machine.html'

    def dispatch(self, request, *args, **kwargs):
        # if list(VendingItems.objects.all()) == []:
        #     VendingItems.objects.create(coke_price=25, pepsi_price=35, soda_price=45, coke_quantity=0,
        #     pepsi_quantity=0, soda_quantity=0)
        if list(VendingMachineMoney.objects.all()) == []:
            VendingMachineMoney.objects.create(m_penny=0, m_nickel=0, m_dime=0, m_quater=0)
        if list(UserMoney.objects.all()) == []:
            UserMoney.objects.create(u_penny=0, u_nickel=0, u_dime=0, u_quater=0)

        return super(DisplayVendingMachine, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # vending_machine_data = VendingItems.objects.get(pk=1)
        vending_machine_items = VendingItemsNew.objects.all()
        return render(self.request, self.template_name, {"data":vending_machine_items})


class SaveValue(View):                   #saves the coins entered by user in database using ajax call

    def get(self, request):
        num = request.GET['num']
        user_money = UserMoney.objects.all().first()
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


class CancelTransaction(View):                   #delete user details and displays message of cancellation 
    
    def get(self, request, *args, **kwargs):
        user_money = UserMoney.objects.all().first()
        to_message = "Transaction cancelled! Here is your "+str(user_money.u_penny)+" penny, "+str(user_money.u_nickel)+" nickel, "+\
                        str(user_money.u_dime)+" dime, "+str(user_money.u_quater)+" quater"
        messages.add_message(request, messages.INFO, to_message)
        UserMoney.objects.all().delete()
        return redirect(reverse_lazy('display_machine'))


class CommitTransaction(View):                   #checks for various conditions of failure and completes the order 
    
    def get(self, request, pk, *args, **kwargs):
        vending_machine_data = VendingItemsNew.objects.get(pk=pk)
        user_money = UserMoney.objects.all().first()
        vending_machine_money = VendingMachineMoney.objects.all().first()
        vending_money_pk=vending_machine_money.pk
        price = vending_machine_data.item_price

        if(vending_machine_data.item_quantity == 0):
            to_message = "Transaction cancelled! Out of Stock. Here is your "+str(user_money.u_penny)+" penny, "+ \
                str(user_money.u_nickel)+" nickel, "+ \
                str(user_money.u_dime)+" dime, "+str(user_money.u_quater)+" quater"
            messages.add_message(request, messages.INFO, to_message)
            user_money.delete()
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
            user_money.delete()
            return redirect(reverse_lazy('display_machine'))

        else:
            VendingMachineMoney.objects.filter(pk=vending_money_pk).update( m_penny=vending_machine_money.m_penny + user_money.u_penny - penny_change,
                                                              m_nickel=vending_machine_money.m_nickel + user_money.u_nickel - nickel_change,
                                                              m_dime=vending_machine_money.m_dime + user_money.u_dime - dime_change,
                                                              m_quater=vending_machine_money.m_quater + user_money.u_quater - quater_change)

            to_message = vending_machine_data.item_name + " pops out! "
            vending_machine_data.item_quantity = vending_machine_data.item_quantity - 1
            vending_machine_data.save()
            to_message += "Here is your " + str(penny_change) + " penny, " + \
                            str(nickel_change) + " nickel, " + \
                            str(dime_change)+" dime, " + str(quater_change) + " quater"
            messages.add_message(request, messages.INFO, to_message)
            user_money.delete()
            return redirect(reverse_lazy('display_machine'))

