from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,),
    path('enroll/', views.enroll_view, name='enroll'),
    path('checkin/', views.checkin_view, name='checkin'),
]
