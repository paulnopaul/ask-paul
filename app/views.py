from django.shortcuts import render
from django.core.paginator import Paginator
import random

from .models import Question, Answer

tags = ['tag1', 'tag2', 'tag3', 'tag4']

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


answers = [
    {
        'id': idx,
        'text': f'answer {idx}',
        'is_correct': True,
    } for idx in range(answer_count)
]

questions = [
    {
        'id': idx,
        'title': f'title {idx}',
        'text': lorem_ipsum,
        'tags': [tags[idx % len(tags)], tags[(idx + 1) % len(tags)]],
        'answers': [random.choice(answers) for i in range(random.randint(1, 10))],
        'like_count': idx
    } for idx in range(question_count)
]


def paginate_objects(objects, page, objects_per_page=20):
    return Paginator(objects, objects_per_page).get_page(page)


def new_questions(request):
    q = paginate_objects(Question.objects.new(),
                         request.GET.get('page'), 11)
    return render(request, 'new_questions.html', {
        'questions': q
    })


def hot_questions(request):
    q = paginate_objects(Question.objects.hot(),
                         request.GET.get('page'), 11)
    return render(request, 'hot_questions.html', {
        'questions': q
    })


def tag_questions(request, t):
    q = paginate_objects(Question.objects.by_tag(t),
                         request.GET.get('page'), 11)
    return render(request, 'tag_page.html', {
        'tag_title': t,
        'questions': q
    })


def question_page(request, pk):
    question = questions[pk]
    answers = paginate_objects(Answer.objects.by_question(pk),
                               request.GET.get('page'), 5)
    return render(request, 'question_page.html', {
        'question': question,
        'questions': answers
    })


def login_page(request):
    return render(request, 'login_page.html', {})


def signup_page(request):
    return render(request, 'signup_page.html', {})


def settings_page(request):
    return render(request, 'settings_page.html', {})


def ask_page(request):
    return render(request, 'ask_page.html', {})
