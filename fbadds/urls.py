from django.urls import path
from . import views


app_name = 'fbadds'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>/', views.singlepage, name='singlepage')
]
