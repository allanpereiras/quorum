"""
URL configuration for app bills.
"""
from django.urls import path
from bills import views

urlpatterns = [
    path('', views.BillsView.as_view(), name="dashboard")
]
