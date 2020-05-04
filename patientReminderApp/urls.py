from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('ptLogReg', views.ptLogReg),
    path('physLogReg', views.physLogReg),
    path('ptDashboard', views.ptDashboard),
    path('physDashboard', views.physDashboard),
    path('ptLogout', views.ptLogout),
    path('physLogout', views.physLogout),
    path('newTask', views.newTask),
    path('ptRegister', views.ptRegister),
    path('physRegister', views.physRegister),
    path('ptLogin', views.ptLogin),
    path('physLogin', views.physLogin),
    path('createTask', views.createTask),
    path('complete/<int:taskID>', views.complete),
    path('delete/<int:taskID>', views.delete),
    path('patient/<int:ptID>', views.ptPage),
]
