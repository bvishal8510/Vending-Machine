from django.db import models

class VendingItems(models.Model):
    coke_price = models.PositiveIntegerField(default=25)
    pepsi_price = models.PositiveIntegerField(default=35)
    soda_price = models.PositiveIntegerField(default=45)
    coke_quantity = models.PositiveIntegerField(default=0)
    pepsi_quantity = models.PositiveIntegerField(default=0)
    soda_quantity = models.PositiveIntegerField(default=0)



class VendingMachineMoney(models.Model):
    m_penny = models.PositiveIntegerField(default=0)
    m_nickel = models.PositiveIntegerField(default=0)
    m_dime = models.PositiveIntegerField(default=0)
    m_quater = models.PositiveIntegerField(default=0)
    



class UserMoney(models.Model):
    u_penny = models.PositiveIntegerField(default=0)
    u_nickel = models.PositiveIntegerField(default=0)
    u_dime = models.PositiveIntegerField(default=0)
    u_quater = models.PositiveIntegerField(default=0)
    

