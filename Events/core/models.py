from shopify_auth.models import AbstractShopUser
from django.db import models

class AuthAppShopUser(AbstractShopUser):
    pass

class Users(models.Model):
    sno = models.AutoField(primary_key = True)
    domain_name = models.CharField(max_length = 100, unique = True)
    flag = models.IntegerField(default = -1)
    def __str__(self):
        return (str(self.domain_name))

class Events(models.Model):
    sno = models.ForeignKey(Users, on_delete=models.CASCADE)
    event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length = 300)
    location    = models.TextField(default="New Delhi")
    description = models.TextField(default="NA")
    start_date  = models.DateField(auto_now=False,auto_now_add=False,default="1997-01-23")
    end_date    = models.DateField(auto_now=False,auto_now_add=False,default="1997-01-23")
    start_time  = models.TimeField(auto_now=False,auto_now_add=False,default="10:10")
    end_time    = models.TimeField(auto_now=False,auto_now_add=False,default="10:10")
    inventory   = models.IntegerField(default=0)
    price       = models.DecimalField(max_digits=19,decimal_places=3,default=0.000)

class Tickets(models.Model):
    sno = models.ForeignKey(Events, on_delete=models.CASCADE)
    ticket_id = models.AutoField(primary_key=True)
    date  = models.DateField(auto_now=False,auto_now_add=False,default="1997-01-23")
    type = models.CharField(max_length = 50)
    price = models.FloatField(default=0.0)

class Customers(models.Model):
    sno = models.ForeignKey(Tickets, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length = 200)
    customer_email = models.CharField(max_length = 200)
    customer_number = models.CharField(max_length = 50)
