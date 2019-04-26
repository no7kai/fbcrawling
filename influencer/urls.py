from django.urls import path
from . import views


app_name = 'influencer'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>/', views.personal, name='personal'),
    path('search/', views.search, name='search'),

]
