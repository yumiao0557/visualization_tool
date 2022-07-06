from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='dashboard-index'),
    path('function1/', views.function1, name='function 1'),

 
  
 
    path('Import_csv/', views.Import_csv,name="Import_csv"), 
    path('UCSD_data_fake/', views.UCSD_data_fake,name="UCSD_data_fake"),
    path('UCSD_data/', views.UCSD_data,name="UCSD_data"),
    path('LSpine_data/', views.LSpine_data,name="LSpine_data"),
    path('product/', views.product,name="dashboard-product"),
    path('staff/', views.staff,name="dashboard-staff"),
    path('order/', views.order,name="dashboard-order"),
     

]