from .models import Events

from django import forms

class createEvent(forms.ModelForm):
    class Meta:
        model = Events
        fields = [
            'event_name',
            'location',
            'description',
            'start_date',
            'end_date',
            'start_time',
            'end_time',
            'inventory',
            'price'
        ]