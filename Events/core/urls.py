from django.urls import path,include
from core import views,dashboard,statistics,customers
from django.conf.urls.static import static
from django.conf import settings

app_name = 'core'

urlpatterns = [
    path('', views.index, name="index"),
    path('create', views.createEventForm, name="createEventForm"),
    path('Dashboard', dashboard.dashboard, name="dashboard"),
    path('Statistics', statistics.statistics, name="statistics"),
    path('Customers', customers.customers, name="customers"),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
