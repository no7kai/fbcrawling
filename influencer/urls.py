from django.urls import path
from . import views


app_name = 'influencer'

urlpatterns = [
    path('', views.index, name='index'),
    path('personal/', views.personal, name='personal'),

]
