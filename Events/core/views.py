from django.shortcuts import render
from django.http import HttpResponse
from .forms import createEvent
# Create your views here.
def index(request):
    return HttpResponse("200")

def createEventForm(request):

    createforms = createEvent(request.POST or None)
    if createforms.is_valid():
        createforms.save()
        createforms = createEvent

    context = {
        'event': createforms
    }

    return render(request,"core/create_event.html",context)
