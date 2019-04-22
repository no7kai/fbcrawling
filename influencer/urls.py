from django.urls import path
from . import views


app_name = 'influencer'
urlpatterns = [
    path('', views.users, name='user'),
    path('<int:user_id>/', views.personal, name='personal'),
    path('searchid/', views.search_by_id, name='searchid'),
    path('searchname/', views.search_by_name, name='searchname'),
    path('searchpost/', views.search_post, name='searchpost'),
    path('<str:from_date>_<str:to_date>/', views.result_post, name='resultpost'),
    path('updateuser/', views.update_user, name='updateuser'),
    path('test/', views.test, name='test'),
    path('updating/', views.updating, name='updating'),
    # path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote')
]
