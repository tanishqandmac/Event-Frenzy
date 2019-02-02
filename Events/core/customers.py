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

# #To be used in Production
# def dashboard1(request):
#     with request.user.session:
#         try:
#             user = Users(domain_name="believer")
#             user.save()
#             user = Users.objects.get(domain_name = "believer")
#             event = Events(sno = user,
#                             event_name = "Dragons",
#                             start_date = "2019-01-28",
#                             end_date = "2019-01-31")
#             event.save()
#             event = Events.objects.filter(sno = user)
#             tickets = Tickets(sno = event[0],
#                               type = "Gold",
#                               price = 100.0)
#             tickets.save()
#             tickets = Tickets.objects.filter(sno = event[0])
#             customer = Customers(sno = tickets[0],
#                                 customer_name = "tanishq",
#                                 customer_email = "tanishqandmac@gmail.com")
#             customer.save()

#             domain_name = str(request.user).split(".")[0]
#             userObject = Users.objects.get(domain_name = domain_name)
#             events = Events.objects.filter(sno = userObject)
#             event_details_list = []
#             for event in events:
#                 event_details = {}
#                 event_name = event['event_name']
#                 start_date = event['start_date']
#                 end_date = event['end_date']
#                 tickets = Tickets.objects.filter(sno=event['event_id'])
#                 tickets_sold = tickets.count()
#                 revenue = sum([ticket['price'] for ticket in tickets])
#                 event_details = {'Name':event_name,
#                                  'Start_Date':start_date,
#                                  'End_Date':end_date,
#                                  'Tickets_Sold':tickets_sold,
#                                  'Revenue':revenue}
#                 event_details_list.append(event_details)
#             print (event_details_list)
#             context = {'Events':event_details_list}
#             return render(request,"core/dashboard.html",context)
#         except:
#             return render(request,"core/error.html",{})
