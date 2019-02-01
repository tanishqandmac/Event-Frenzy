from django.shortcuts import render
from django.http import HttpResponse
from .forms import createEvent
# Create your views here.
def index(request):

    createforms = createEvent(request.POST or None)
    if createforms.is_valid():
        createforms.save()

    context = {
        'event': createforms
    }

    return render(request,"core/create_event.html",context)
