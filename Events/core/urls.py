from django.urls import path,include
from core import views,dashboard
from django.conf.urls.static import static
from django.conf import settings

app_name = 'core'

urlpatterns = [
    path('', views.index, name="index"),
    path('dashboard', dashboard.dashboard, name="dashboard"),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
