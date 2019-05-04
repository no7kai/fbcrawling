from django.shortcuts import render, get_object_or_404
from .models import Page, Adds
from django.core.paginator import Paginator
from .forms import FindForm
from .get_adsid import get_adsid
from .get_adslsc import get_adslsm
from django.http import HttpResponseRedirect
from django.urls import reverse
from .filter import PageFilter

# Create your views here.


def index(request):
    title = 'Facebook Beauty Pages'
    pages = Page.objects.all()
    page_filter = PageFilter(request.GET, queryset=pages)
    paginator = Paginator(page_filter.qs, 15)
    page = request.GET.get('page')
    context = {
        'title': title,
        'filter': page_filter,
        'queryset': paginator.get_page(page)
    }
    return render(request, 'fbadds/index.html', context)


def singlepage(request, slug):
    page = get_object_or_404(Page, slug=slug)
    ads = page.adds_set.all()
    context = {'page': page, 'ads': ads}
    return render(request, 'fbadds/singlepage.html', context)


def find(request):
    form = FindForm(request.POST or None)
    if form.is_valid():
        pageid = form.cleaned_data['find']
        form = FindForm()
        list_id = get_adsid(pageid)
        if type(list_id) is str:
            context = {'form': form, 'error': list_id}
            return render(request, 'fbadds/find.html', context)
        get_adslsm(pageid, list_id)
        page = get_object_or_404(Page, pageid=pageid)
        slug = page.slug
        return HttpResponseRedirect(reverse('fbadds:singlepage', args=(slug,)))
    context = {'form': form}
    return render(request, 'fbadds/find.html', context)
