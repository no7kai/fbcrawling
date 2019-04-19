from django.shortcuts import render, get_object_or_404
from .models import User, Post
from .forms import SearchIdForm, SearchNameForm
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.


def users(request):
    top_users = User.objects.order_by('-followers')[:10]
    context = {'top_users': top_users}
    return render(request, 'influencer/index.html', context)


def personal(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    top_posts = user.post_set.order_by('created')[:10]
    context = {'top_posts': top_posts, 'user': user}
    return render(request, 'influencer/personal.html', context)


def search_by_id(request):
    if request.method == "POST":
        form = SearchIdForm(request.POST)
        if form.is_valid():
            uid = form.cleaned_data['uid']
            user = get_object_or_404(User, uid=uid)
            return HttpResponseRedirect(reverse('influencer:personal', args=(user.id,)))
    else:
        form = SearchIdForm()

    return render(request, 'influencer/search.html', {'form': form})


def search_by_name(request):
    if request.method == "POST":
        form = SearchNameForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            users = User.objects.filter(name__contains=name).order_by('-followers')
            context = {'users': users}
            return render(request, 'influencer/listname.html', context)
    else:
        form = SearchNameForm()

    return render(request, 'influencer/search.html', {'form': form})


