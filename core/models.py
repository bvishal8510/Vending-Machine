from django.db import models

class VendingItems(models.Model):                             #store data of items in vending machine
    coke_price = models.PositiveIntegerField(default=25)
    pepsi_price = models.PositiveIntegerField(default=35)
    soda_price = models.PositiveIntegerField(default=45)
    coke_quantity = models.PositiveIntegerField(default=0)
    pepsi_quantity = models.PositiveIntegerField(default=0)
    soda_quantity = models.PositiveIntegerField(default=0)


class VendingItemsNew(models.Model):
    item_name = models.CharField(blank=False, unique=True, max_length=200)
    item_price = models.PositiveIntegerField()
    item_quantity = models.PositiveIntegerField()


class VendingMachineMoney(models.Model):                             #store data of money in vending machine
    m_penny = models.PositiveIntegerField(default=0)
    m_nickel = models.PositiveIntegerField(default=0)
    m_dime = models.PositiveIntegerField(default=0)
    m_quater = models.PositiveIntegerField(default=0)
    

class UserDetails(models.Model):
    item_name = models.ForeignKey(VendingItemsNew, on_delete=models.CASCADE)
    time_of_purchase = models.DateTimeField()

class UserMoney(models.Model):                             #store data of user's money for each transaction
    u_penny = models.PositiveIntegerField(default=0)
    u_nickel = models.PositiveIntegerField(default=0)
    u_dime = models.PositiveIntegerField(default=0)
    u_quater = models.PositiveIntegerField(default=0)
    

