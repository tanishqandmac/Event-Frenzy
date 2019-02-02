from .models import Users,Events,Tickets,Customers
from django.views.decorators.csrf import csrf_exempt
from shopify_auth.decorators import login_required
from shopify_auth.models import AbstractShopUser, ShopUserManager
from django.http import HttpResponse
from django.shortcuts import render, redirect
import matplotlib.pyplot as plt
from django.db.models import Sum
from django.contrib import auth
from datetime import datetime
from django_rq import job
import traceback
import requests
import shopify
import time
import os

def statistics(request):
    try:
        Users.objects.all().delete()
        Events.objects.all().delete()
        Tickets.objects.all().delete()
        Customers.objects.all().delete()
        user = Users(domain_name="believer")
        user.save()
        user = Users.objects.get(domain_name = "believer")
        for i in range(10):
            event = Events(sno = user,
                            event_name = "Dragons {}".format(i),
                            start_date = "2019-01-28",
                            end_date = "2019-01-31")
            event.save()
        events = Events.obejects.filter(sno=user)
        for e in events:
            for i in range(10):
                tickets = Tickets(sno = e,
                                type = "Platinum",
                                price = 3000.0 + float(i))
                tickets.save()
                for k in range(10):
                    customer = Customers(sno = tickets,
                                        customer_name = "tanishq",
                                        customer_email = "tanishqandmac@gmail.com")
                    customer.save()

        #domain_name = str(request.user).split(".")[0]
        domain_name = "believer"
        userObject = Users.objects.get(domain_name = domain_name)
        events = Events.objects.filter(sno = userObject)
        event_details_list = []
        for event in events:
            event_details = {}
            event_name = event.event_name
            start_date = event.start_date
            end_date = event.end_date
            inventory = event.inventory
            tickets = Tickets.objects.filter(sno=event)
            tickets_sold = tickets.count()
            revenue = sum([ticket.price for ticket in tickets])
            
            names='Tickets Sold', 'Inventory',
            size=[tickets_sold,inventory-tickets_sold]
            my_circle=plt.Circle( (0,0), 0.7, color='white')
            plt.pie(size, labels=names, colors=['green','red'])
            p=plt.gcf()
            p.gca().add_artist(my_circle)

            event_details = {'Name':event_name,
                             'Start_Date':date_to_string([str(start_date)]),
                             'End_Date':date_to_string([str(end_date)]),
                             'Tickets_Sold':tickets_sold,
                             'Inventory': inventory,
                             'Revenue':revenue}
            event_details_list.append(event_details)
        print (event_details_list)
        context = {'Events':event_details_list}
        return render(request,"core/statistics.html",context)
    except Exception:
        print(traceback.format_exc())
        return render(request,"core/error.html",{})

def date_to_string(dates):
    date = datetime.strptime(dates[0].split(" ")[0], '%Y-%m-%d')
    date = str(date.strftime('%B %d, %Y'))
    try:
        if dates[1].split(" ")[0] != dates[0].split(" ")[0]:
            date2 = datetime.strptime(dates[1].split(" ")[0], '%Y-%m-%d')
            date2 = str(date2.strftime('%B %d, %Y'))
            date = date + " - " + date2
    except:
        pass
    return date

#To be used in Production
def dashboard1(request):
    with request.user.session:
        try:
            user = Users(domain_name="believer")
            user.save()
            user = Users.objects.get(domain_name = "believer")
            event = Events(sno = user,
                            event_name = "Dragons",
                            start_date = "2019-01-28",
                            end_date = "2019-01-31")
            event.save()
            event = Events.objects.filter(sno = user)
            tickets = Tickets(sno = event[0],
                              type = "Gold",
                              price = 100.0)
            tickets.save()
            tickets = Tickets.objects.filter(sno = event[0])
            customer = Customers(sno = tickets[0],
                                customer_name = "tanishq",
                                customer_email = "tanishqandmac@gmail.com")
            customer.save()

            domain_name = str(request.user).split(".")[0]
            userObject = Users.objects.get(domain_name = domain_name)
            events = Events.objects.filter(sno = userObject)
            event_details_list = []
            for event in events:
                event_details = {}
                event_name = event['event_name']
                start_date = event['start_date']
                end_date = event['end_date']
                tickets = Tickets.objects.filter(sno=event['event_id'])
                tickets_sold = tickets.count()
                revenue = sum([ticket['price'] for ticket in tickets])
                event_details = {'Name':event_name,
                                 'Start_Date':start_date,
                                 'End_Date':end_date,
                                 'Tickets_Sold':tickets_sold,
                                 'Revenue':revenue}
                event_details_list.append(event_details)
            print (event_details_list)
            context = {'Events':event_details_list}
            return render(request,"core/dashboard.html",context)
        except:
            return render(request,"core/error.html",{})
