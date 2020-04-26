from django.urls import path
from . import views

urlpatterns = [
    path('', views.DisplayVendingMachine.as_view(), name='display_machine'),
    path('save', views.SaveValue.as_view(), name='save_value'),
    path('commit/<int:pk>', views.CommitTransaction.as_view(), name='commit'),
    path('cancel', views.CancelTransaction.as_view(), name='cancel'),
]
