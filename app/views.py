from django.shortcuts import render
import random

tags = ['tag1', 'tag2', 'tag3', 'tag4']

lorem_ipsum = '''Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed 
do eiusmod tempor incididunt ut labore et dolore magna 
aliqua. Ut enim ad minim veniam, quis nostrud exercitation 
ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis 
aute irure dolor in reprehenderit in voluptate velit esse cillum 
dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat 
non proident, sunt in culpa qui officia deserunt mollit anim id 
est laborum.'''

questions = [
        {
            'id': idx,
            'title': f'title {idx}',
            'text': lorem_ipsum,
            'tags': [tags[idx % len(tags)], tags[(idx + 1) % len(tags)]]
        } for idx in range(10)
        ]


def new_questions(request):
    return render(request, 'new_questions.html', {
        'questions': questions, 
        })

def hot_questions(request):
    return render(request, 'hot_questions.html', {})

def tag_questions(request, t):
    tquestions = list(filter(lambda x: t in x['tags'], questions))
    return render(request, 'tag_page.html', {
        'tag_name':  t,
        'questions': tquestions,
        })

def question_page(request, pk):
    question = questions[pk]
    return render(request, 'question_page.html', {
        'question': question
        })
