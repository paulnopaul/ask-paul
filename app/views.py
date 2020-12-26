from django.shortcuts import render, redirect
from django.core.paginator import Paginator
import random

from .models import Question, Answer, Tag

from app.forms import LoginForm
from django.contrib import auth

lorem_ipsum = '''Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed 
do eiusmod tempor incididunt ut labore et dolore magna 
aliqua. Ut enim ad minim veniam, quis nostrud exercitation 
ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis 
aute irure dolor in reprehenderit in voluptate velit esse cillum 
dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat 
non proident, sunt in culpa qui officia deserunt mollit anim id 
est laborum.'''

question_count = 200
questions_per_page = 11
answer_count = 10


def paginate_objects(objects, page, objects_per_page=20):
    return Paginator(objects, objects_per_page).get_page(page)


def new_questions(request):
    return render(request, 'new_questions.html', {
        'questions': paginate_objects(Question.objects.new(),
                         request.GET.get('page'), 11),
        'popular_tags': Tag.objects.popular()

    })


def hot_questions(request):
    q = paginate_objects(Question.objects.hot(),
                         request.GET.get('page'), 11)
    return render(request, 'hot_questions.html', {
        'questions': q,
        'popular_tags': Tag.objects.popular()
    })


def tag_questions(request, t):
    q = paginate_objects(Question.objects.by_tag(t),
                         request.GET.get('page'), 11)
    return render(request, 'tag_page.html', {
        'tag_title': t,
        'questions': q,
        'popular_tags': Tag.objects.popular()
    })


def question_page(request, pk):
    question = Question.objects.get(pk=pk)
    answers = paginate_objects(Answer.objects.by_question(pk),
                               request.GET.get('page'), 5)
    return render(request, 'question_page.html', {
        'question': question,
        'questions': answers,
        'popular_tags': Tag.objects.popular()
    })


def logout(request):
    auth.logout(request)
    return redirect("/") # TODO нужны правильный редиректы (на предыдущую страницу)


def login_page(request):
    if request.method == 'GET':
        form = LoginForm()
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                return redirect("/") # TODO нужны правильный редиректы (на предыдущую страницу)

    ctx = {'form': form}
    return render(request, 'login_page.html', ctx)


def signup_page(request):
    return render(request, 'signup_page.html', {})


def settings_page(request):
    return render(request, 'settings_page.html', {})


def ask_page(request):
    return render(request, 'ask_page.html', {})
