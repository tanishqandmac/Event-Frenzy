from .models import Users,Events,Tickets,Customers
from django.views.decorators.csrf import csrf_exempt
from shopify_auth.decorators import login_required
from shopify_auth.models import AbstractShopUser, ShopUserManager
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Sum
from django.contrib import auth
from datetime import datetime
from django_rq import job
import traceback
import requests
import shopify
import time
import os

def customers(request):
    try:
        #Data Generation
        Users.objects.all().delete()
        user = Users(domain_name="believer")
        user.save()
        for i in range(5):
            user = Users.objects.get(domain_name="believer")
            event = Events(sno=user,
                            event_name = "Dragons {}".format(i),
                            start_date = "2019-01-28",
                            end_date = "2019-01-31")
            event.save()
            event = Events.objects.filter(sno = user)
            tickets = Tickets(sno = event[i],
                              type = "Platinum",
                              price = 3000.0 + float(i))
            tickets.save()
            tickets = Tickets.objects.filter(sno = event[i])
            customer = Customers(sno = tickets[0],
                                customer_name = "tanishq",
                                customer_email = "tanishqandmac@gmail.com")
            customer.save()


        customers_list = []
        event_id = request.GET.get('event_id', '')
        #event = Events.objects.get(event_id = event_id)
        event = Events.objects.all()[0]
        tickets = Tickets.objects.filter(sno = event)
        i = 1
        for ticket in tickets:
            customers = Customers.objects.filter(sno = ticket)
            for customer in customers:

                customer_details = {'Sno':i,
                                    'Name':customer.customer_name,
                                    'Email':customer.customer_email,
                                    'Number':customer.customer_number,
                                    'Category':ticket.type}
                i+=1
                customers_list.append(customer_details)
        return render(request,"core/customers.html",{"Customers":customers_list})
    except Exception:
        print(traceback.format_exc())
        return render(request,"core/error.html",{})
