from django.urls import path
from our_browser import views

urlpatterns = [
    path('', views.our_browser, name='our_browser'),
]