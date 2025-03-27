from django.http import Http404
from django.shortcuts import render, redirect
from MainApp.models import Snippet
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseNotFound

def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    context = {'pagename': 'Добавление нового сниппета'}
    return render(request, 'pages/add_snippet.html', context)


def snippets_page(request):
    snippets = Snippet.objects.all()
    context = {'pagename': 'Просмотр сниппетов',
               'snippets': snippets}
    return render(request, 'pages/view_snippets.html', context)

def snippets_detail(request, id):
    try:
        snippet = Snippet.objects.get(pk=id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound(f"<b>Сниппет не найден</b>")
    else:
        context = {'snippet': snippet,
                   'pagename': 'Описание сниппета'}
        return render(request, 'pages/snippet_detail.html', context) 
