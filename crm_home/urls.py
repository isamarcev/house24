from django.urls import path, include
from . import views

app_name = 'crm_home'
urlpatterns = [
    path('set-services/', views.ServiceSettings.as_view(), name='set_services'),

]