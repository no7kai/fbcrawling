from django.shortcuts import render
from .models import Page, Adds
from django.core.paginator import Paginator
# Create your views here.


def index(request):
    title = 'Facebook Beauty Pages'
    pages = Page.objects.all()
    paginator = Paginator(pages, 15)
    page = request.GET.get('page')
    context = {
        'title': title,
        'pages': paginator.get_page(page)
    }
    return render(request, 'fbadds/index.html', context)


def singlepage(request, id):
    page = Page.objects.get(id=id)
    ads = page.adds_set.all()
    context = {'page': page, 'ads': ads}
    return render(request, 'fbadds/singlepage.html', context)
