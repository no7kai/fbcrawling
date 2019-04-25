from django.shortcuts import render, get_object_or_404
from .models import Influencer, Post
from .forms import SearchIdForm, SearchNameForm, SearchPost, UpdateUserForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
import os
from .updateuser import updateuser
# Create your views here.


def index(request):
    top_users = Influencer.objects.order_by('-followers')[:50]
    paginator = Paginator(top_users, 15)
    page = request.GET.get('page')
    context = {'top_users': paginator.get_page(page)}
    return render(request, 'influencer/index.html', context)


def personal(request, user_id):
    user = get_object_or_404(Influencer, pk=user_id)
    top_posts = user.post_set.order_by('created')[:10]
    context = {'top_posts': top_posts, 'user': user}
    return render(request, 'influencer/personal.html', context)


def search_by_id(request):
    if request.method == "POST":
        form = SearchIdForm(request.POST)
        if form.is_valid():
            uid = form.cleaned_data['uid']
            try:
                user = Influencer.objects.get(uid=uid)
            except Influencer.DoesNotExist:
                return HttpResponseRedirect(reverse('influencer:updateuser'))
            return HttpResponseRedirect(reverse('influencer:personal', args=(user.id,)))
    else:
        form = SearchIdForm()

    return render(request, 'influencer/search.html', {'form': form})


def search_by_name(request):
    if request.method == "POST":
        form = SearchNameForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            users = Influencer.objects.filter(name__contains=name).order_by('-followers')
            context = {'users': users}
            return render(request, 'influencer/listname.html', context)
    else:
        form = SearchNameForm()

    return render(request, 'influencer/search.html', {'form': form})


def search_post(request):
    if request.method == "POST":
        form = SearchPost(request.POST)
        if form.is_valid():
            date = form.cleaned_data
            return HttpResponseRedirect(reverse('influencer:resultpost', kwargs=date))
    else:
        form = SearchPost()

    return render(request, 'influencer/search.html', {'form': form})


def result_post(request, from_date, to_date):
    posts = Post.objects.filter(created__gte=from_date).filter(created__lte=to_date)[:50]
    paginator = Paginator(posts, 15)
    page = request.GET.get('page')
    context = {'posts': paginator.get_page(page)}
    return render(request, 'influencer/listpost.html', context)


def update_user(request):
    form = UpdateUserForm(request.POST or None)
    if form.is_valid():
        uid = form.cleaned_data['uid']
        from_date = form.cleaned_data['from_date']
        to_date = form.cleaned_data['to_date']
        updateuser(uid, from_date, to_date)
        return HttpResponseRedirect(reverse('influencer:updating'))
    return render(request, 'influencer/updateuser.html', {'form': form})
