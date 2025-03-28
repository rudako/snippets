from django.http import Http404, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, render, redirect
from MainApp.models import Snippet
from .forms import SnippetForm, UserRegistrationForm, CommentForm
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib import auth
from django.contrib.auth.decorators import login_required


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)

@login_required(login_url='home')
def add_snippet_page(request):
    #Создаем пустую форму при запросе методом GET
    if request.method == 'GET':
        form = SnippetForm()
        context = {
            'pagename': 'Добавление нового сниппета',
            'form': form,}
        return render(request, 'pages/add_snippet.html', context)
    
    # Получаем данные из формы и на их основе создаем новый snippet в БД
    if request.method == 'POST':
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet=form.save(commit=False)
            if request.user.is_authenticated:
                snippet.user = request.user
                snippet.save()
            return redirect("sn_list")
        return render(request, "pages/add_snippet.html", {'form': form})

@login_required()
def my_snippets(request):
    snippets = Snippet.objects.filter(user=request.user)
    context = {'pagename': 'Мои сниппеты',
               'snippets': snippets}
    return render(request, 'pages/view_snippets.html', context)

def snippets_page(request):
    snippets = Snippet.objects.filter(public=True)
    context = {'pagename': 'Просмотр сниппетов',
               'snippets': snippets,
               'count': snippets.count()
               }
    return render(request, 'pages/view_snippets.html', context)

def snippets_detail(request, id):
    context = {'pagename': 'Просмотр сниппета'}
    try:
        snippet = Snippet.objects.get(pk=id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound(f"<b>Сниппет не найден</b>")
    else:
        comments_form = CommentForm()
        context['snippet'] = snippet
        context['type'] = 'view'
        context['comments_form'] = comments_form


        return render(request, 'pages/snippet_detail.html', context) 

@login_required
def snippets_edit(request, id):
    context = {'pagename': 'Редактирование сниппета'}
    try:
        snippet = Snippet.objects.filter(user=request.user).get(pk=id)
    except ObjectDoesNotExist:
        return Http404
    # Хотим получить страницу с данными сниппета
    if request.method == 'GET':
        context = {
            'snippet': snippet,
            'type': 'edit',
            }
        return render(request, 'pages/snippet_detail.html', context)
    
    # Получаем данные из формы и на их основе создаем новый snippet в БД
    if request.method == 'POST':
        data_form = request.POST
        snippet.name = data_form['name']
        # snippet.lang = data_form['lang']
        snippet.code = data_form['code']
        #Если ключ public есть в словаре, берем значкение. Если нет - присваеваем False
        snippet.public = data_form.get('public', False)
        snippet.creation_date = data_form['creation_date']
        snippet.save()
        return redirect("sn_list")

@login_required
def snippets_delete(request, id):
    if request.method == "POST" or request.method == "GET":
        snippet = get_object_or_404(Snippet.objects.filter(user=request.user), id=id)
        snippet.delete()
    return redirect('sn_list')


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        # print("username=", username)
        # print("password=", password)
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            # Return error message
            context = {
                "pagename": "PythonBin",
                "errors": ['wrong username or password'],
            }
            return render(request, 'pages/index.html', context)
    return redirect('home')
#return redirect(request.META.get('HTTP_REFERER', '/'))


def create_user(request):
    context = {
        'pagename': 'Регистрация нового пользователя'}
    #Создаем пустую форму при запросе методом GET
    if request.method == 'GET':
        form = UserRegistrationForm()
        context['form'] = form
        return render(request, 'pages/registration.html', context)
    
    # Получаем данные из формы и на их основе создаем новый snippet в БД
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
        context['form'] = form
        return render(request, "pages/registration.html", context)
    

def logout(request):
    auth.logout(request)
    return redirect('home')

@login_required
def comments_add(request):
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            snippet_id = request.POST.get('snippet_id')
            snippet = Snippet.objects.get(id=snippet_id)
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.snippet = snippet
            comment.save()
            return redirect("sn_detail", id=snippet_id)
    return HttpResponseNotAllowed(['POST'])