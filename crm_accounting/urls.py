from django.urls import path, include
from . import views

app_name = 'crm_accounting'

urlpatterns = [

    # accounts
    path('account/detail/<int:pk>/', views.main_page, name='account_detail'),


]