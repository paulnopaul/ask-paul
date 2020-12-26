from django.core.management.base import BaseCommand
from app.models import Tag, Answer, Question, Profile, QuestionLike, AnswerLike
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from random import choice, randint, sample
from faker import Faker


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=100)
        parser.add_argument('--tags', type=int, default=100)
        parser.add_argument('--questions', type=int, default=100)
        parser.add_argument('--answers', type=int, default=100)
        parser.add_argument('--qlikes', type=int, default=100)
        parser.add_argument('--alikes', type=int, default=100)

    def handle(self, *args, **options):
        self.clear()
        self.user_count = options['users']
        self.tag_count = options['tags']
        self.question_count = options['questions']
        self.answer_count = options['answers']
        self.alike_count = options['alikes']
        self.qlike_count = options['qlikes']

        self.user_ids = []
        self.f = Faker()

        get_user_model().objects.create_superuser('admin', '', 'password')
        get_user_model().objects.create_user('user', '', 'xxx')
        self.create_users()
        self.create_tags()
        self.create_questions()
        self.create_answers()
        self.create_question_likes()
        self.create_answer_likes()

    def clear(self):
        QuestionLike.objects.all().delete()
        AnswerLike.objects.all().delete()
        Tag.objects.all().delete()
        Answer.objects.all().delete()
        Question.objects.all().delete()
        Profile.objects.all().delete()
        User.objects.all().delete()

    def create_users(self):
        print(self.user_count, "Users")
        for i in range(self.user_count):
            rname = self.f.user_name()
            User(username=''.join(self.f.words(2)), email=self.f.email(),
                 first_name=self.f.first_name(), password=self.f.password()).save()
        self.user_ids = list(User.objects.values_list('id', flat=True))

    def create_tags(self):
        print(self.tag_count, "Tags")
        for i in range(self.tag_count):
            Tag(title=self.f.word() + '_' + self.f.word()).save()

    def create_questions(self):
        print(self.question_count, "Questions")
        tag_ids = list(Tag.objects.values_list('id', flat=True))
        for i in range(self.question_count):
            q = Question(user_id=choice(self.user_ids),
                         title=self.f.sentence(),
                         text=self.f.text(max_nb_chars=2000))

            q.save()


            for x in sample(tag_ids, randint(2, 5)):
                q.tags.add(Tag.objects.get(id=x))
                t = Tag.objects.get(id=x)
                t.question_count += 1
                t.save()
            # q.tags.add(*Tag.objects.get("?")[:random.randint(1, 5)])

    def create_answers(self):
        print(self.answer_count, "Answers")
        question_ids = list(Question.objects.values_list('id', flat=True))
        for i in range(self.answer_count):
            q_id = choice(question_ids)
            a = Answer(user_id=choice(self.user_ids),
                       question_id=q_id,
                       text=self.f.text(max_nb_chars=1000)
                       )
            q = Question.objects.get(pk=q_id)
            q.answer_count += 1
            q.save()
            a.save()

    def create_answer_likes(self):
        print(self.alike_count, "Answer likes")
        answer_ids = list(Answer.objects.values_list('id', flat=True))
        for i in range(self.alike_count):
            a_id = choice(answer_ids)
            a = AnswerLike(user_id=choice(self.user_ids),
                           answer_id=a_id,
                           is_upvote=self.f.boolean()
                           )
            ans = Answer.objects.get(id=a_id)
            ans.like_count += 1 if a.is_upvote else -1

            a.save()
            ans.save()
            

    def create_question_likes(self):
        print(self.qlike_count, "Question likes")
        question_ids = list(Question.objects.values_list('id', flat=True))
        for i in range(self.qlike_count):
            q_id = choice(question_ids)
            a = QuestionLike(user_id=choice(self.user_ids),
                             question_id=q_id,
                             is_upvote=self.f.boolean())

            q = Question.objects.get(pk=q_id)
            q.like_count += 1 if a.is_upvote else -1
            a.save()
            q.save()
