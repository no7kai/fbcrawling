from django.shortcuts import render
from .models import User, Post
# Create your views here.


def users(request):
    top_users = User.objects.order_by('followers')[:10]
    context = {'top_users': top_users}
    return render(request, 'influencer/index.html', context)
