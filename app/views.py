from django.shortcuts import render

questions = [
    {
        'id': idx,
        'title': f'title {idx}',
        'text': 'text text',
    } for idx in range(10)
]


def new_questions(request):
    return render(request, 'new_questions.html', {
        'questions': questions,
    })


def hot_questions(request):
    return render(request, 'hot_questions.html', {})


def login_page(request):
    return render(request, 'login_page.html', {})


def settings_page(request):
    return render(request, 'settings_page.html', {})


def question_page(request, pk):
    question = questions[pk]
    return render(request, 'question_page.html', {
        'question': question
    })
