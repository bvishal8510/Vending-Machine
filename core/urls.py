from django.urls import path
from . import views

urlpatterns = [
    path('', views.DisplayVendingMachine.as_view(), name='display_machine'),
]
