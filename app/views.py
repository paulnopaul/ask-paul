from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from django.contrib import messages

from .models import Question, Answer, Tag

from app.forms import *
from django.contrib import auth
from django.contrib.auth.decorators import login_required

questions_per_page = 11
answer_count = 10


def paginate_objects(objects, page, objects_per_page=20):
    return Paginator(objects, objects_per_page).get_page(page)


def new_questions(request):
    return render(request, 'new_questions.html', {
        'questions': paginate_objects(Question.objects.new(),
                                      request.GET.get('page'), 11),
        'popular_tags': Tag.objects.all()[:20]

    })


def hot_questions(request):
    q = paginate_objects(Question.objects.hot(),
                         request.GET.get('page'), 11)
    return render(request, 'hot_questions.html', {
        'questions': q,
        'popular_tags': Tag.objects.all()[:20]
    })


def tag_questions(request, t):
    q = paginate_objects(Question.objects.by_tag(t),
                         request.GET.get('page'), 11)
    return render(request, 'tag_page.html', {
        'tag_title': t,
        'questions': q,
        'popular_tags': Tag.objects.all()[:20]
    })


def question_page(request, qid):
    question = Question.objects.get(pk=qid)
    answers = paginate_objects(Answer.objects.by_question(qid),
                               request.GET.get('page'), 5)
    return render(request, 'question_page.html', {
        'question': question,
        'questions': answers,
        'popular_tags': Tag.objects.all()[:20]
    })


@login_required
def logout(request):
    auth.logout(request)
    prev_page = request.META.get("HTTP_REFERER")
    if prev_page is not None:
        return redirect(prev_page)
    return redirect("/")  # TODO нужны правильный редиректы (на предыдущую страницу)


def login_page(request):
    if request.method == 'GET':
        form = LoginForm()
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                return redirect("/")  # TODO нужны правильный редиректы (на предыдущую страницу)
            else:
                messages.error(request, 'invalid user or password')
                return redirect(request.POST.get('next', '/'))
    ctx = {'form': form}
    return render(request, 'login_page.html', ctx)


def signup_page(request):
    if request.method == 'GET':
        form = UserSignupForm()
    else:
        form = UserSignupForm(data=request.POST)
        if form.is_valid() and form.password == form.confirm_password:
            form.save()
            return redirect(request.POST.get('next', '/'))
        else:
            messages.error(request, 'something went wrong')
            return redirect('/signup')

    ctx = {'form': form}
    return render(request, 'signup_page.html', ctx)


def settings_page(request):
    return render(request, 'settings_page.html', {})


@login_required
def ask_page(request):
    if request.method == 'GET':
        form = AskForm()
    else:
        form = AskForm(data=request.POST)
        if form.is_valid():
            question = form.save(user=request.user, commit=False)
            return redirect(reverse('question', kwargs={'qid': question.pk}))
        else:
            messages.error(request, 'something went wrong')
            return redirect('ask')

    ctx = {'form': form}
    return render(request, 'ask_page.html', ctx)
