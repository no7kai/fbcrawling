from django.shortcuts import render, get_object_or_404
from .models import Influencer, Post
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
import os
from .filters import PostFilter
# Create your views here.


def index(request):
    title = "Index"
    top_users = Influencer.objects.order_by('-followers')[:50]
    paginator = Paginator(top_users, 15)
    page = request.GET.get('page')
    context = {'title': title, 'top_users': paginator.get_page(page)}
    return render(request, 'influencer/index.html', context)


def personal(request, id):
    title = "Personal"
    user = get_object_or_404(Influencer, pk=id)
    top_posts = user.post_set.order_by('created')[:10]
    context = {'top_posts': top_posts, 'user': user, 'title': title}
    return render(request, 'influencer/personal.html', context)


def search(request):
    post_list = Post.objects.all()
    post_filter = PostFilter(request.GET, queryset=post_list)
    return render(request, 'influencer/post_list.html', {'filter': post_filter})

