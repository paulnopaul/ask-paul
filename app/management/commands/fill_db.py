from django.core.management.base import BaseCommand
from app.models import Tag, Answer, Question, Profile, QuestionLike, AnswerLike
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

import random
import string


def random_username():
    return ''.join(random.sample(string.ascii_letters, random.randint(5, 10)))


def random_name():
    return random.sample(string.ascii_uppercase, 1)[0] + \
        ''.join(random.sample(string.ascii_lowercase, random.randint(3, 6)))


def random_text(word_count):
    words = [''.join(random.sample(string.ascii_lowercase,
                                   random.randint(3, 8))) for _ in range(100)]
    return ' '.join([random.sample(words, 1)[0] for _ in range(word_count)])


class Command(BaseCommand):
    user_count = 10
    question_count = 100
    answer_count = 1000
    like_count = 1000
    tag_count = 10

    def clear(self):
        Tag.objects.all().delete()
        Answer.objects.all().delete()
        Question.objects.all().delete()
        Profile.objects.all().delete()
        QuestionLike.objects.all().delete()
        AnswerLike.objects.all().delete()
        User.objects.all().delete()

    def create_users(self):
        print("Users")
        for i in range(self.user_count):
            rname = random_username()
            User(username=rname, email=rname + "@a.a",
                 first_name="John", password="1111").save()

    def create_tags(self):
        print("Tags")
        for i in range(self.tag_count):
            Tag(title=random_username()).save()

    def create_questions(self):
        print("Questions")
        for i in range(self.question_count):
            q = Question(user=User.objects.order_by("?").first(),
                         title=random_name(),
                         like_count=random.randint(-100, 100),
                         text=random_text(random.randint(100, 1000)),
                         )
            q.save()
            q.tags.add(*Tag.objects.order_by("?")[:random.randint(1, 5)])

    def create_answers(self):
        print("Answers")
        for i in range(self.answer_count):
            a = Answer(user=User.objects.order_by("?").first(),
                       question=Question.objects.order_by("?").first(),
                       like_count=random.randint(-100, 100),
                       text=random_text(random.randint(50, 200)),
                       )
            a.save()

    def create_answer_likes(self):
        print("Answer likes")
        answer_count = Answer.objects.count()
        user_count = User.objects.count()
        for i in range(self.answer_count):
            a = AnswerLike(user=User.objects.get(pk=random.randint(1, user_count)),
                           answer=Answer.objects.get(pk=random.randint(1, answer_count)),
                           is_upvote=bool(random.randint(0, 1))
                           )
            a.save()

    def create_question_likes(self):
        print("Question likes")
        question_count = Question.objects.count()
        user_count = User.objects.count()
        for i in range(self.answer_count):
            a = QuestionLike(user=User.objects.get(pk=random.randint(1,
                                                                     user_count)),
                             question=Question.objects.get(pk=random.randint(1,
                                                                             question_count)),
                             is_upvote=bool(random.randint(0, 1)))
            a.save()

    def handle(self, *args, **options):
        self.clear()
        get_user_model().objects.create_superuser('admin', '', 'password')
        self.create_users()
        self.create_tags()
        self.create_questions()
        self.create_answers()
        self.create_question_likes()
        self.create_answer_likes()
