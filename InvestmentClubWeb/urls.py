from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index.html', views.index, name='index'),
    path('stocks', views.stocks, name='stocks'),
    path('teampage', views.teampage, name='teampage'),
    path('dues', views.dues, name='dues'),
]