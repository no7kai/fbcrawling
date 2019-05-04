from django.urls import path
from . import views


app_name = 'fbadds'

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<slug:slug>/', views.singlepage, name='singlepage'),
    path('find/', views.find, name='find'),
]
