from shopify_auth.models import AbstractShopUser
from django.db import models

class AuthAppShopUser(AbstractShopUser):
    pass

class Users(models.Model):
    sno = models.AutoField(primary_key = True)
    domain_name = models.CharField(max_length = 100, unique = True)
    flag = models.IntegerField(default = -1)
    def __str__(self):
        return (str(self.domainName))

class Events(models.Model):
    sno = models.ForeignKey(Users, on_delete=models.CASCADE)
    event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length = 300)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

class Tickets(models.Model):
    sno = models.ForeignKey(Events, on_delete=models.CASCADE)
    ticket_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length = 50)
    price = models.FloatField(default=0.0)

class Customers(models.Model):
    sno = models.ForeignKey(Tickets, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length = 200)
    customer_email = models.CharField(max_length = 200)
    customer_number = models.CharField(max_length = 50)
