from .models import Users,Events

def dashboard(request):
    with request.user.session:
        try:
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
            context = {'Events':event_details_list}
            return render(request,"core/dashboard.html",context)
        except:
            return render(request,"core/error.html",{})
