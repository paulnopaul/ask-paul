from django.core.management.base import BaseCommand
from app.models import Tag, Answer, Question, Profile, QuestionLike, AnswerLike
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from random import choice, sample, randint
from itertools import islice
from faker import Faker


def clear():
    QuestionLike.objects.all().delete()
    AnswerLike.objects.all().delete()
    Tag.objects.all().delete()
    Answer.objects.all().delete()
    Question.objects.all().delete()
    Profile.objects.all().delete()
    User.objects.all().delete()


def save_bulk(batch_size, objects, model):
    while True:
        batch = list(islice(objects, batch_size))
        if not batch:
            break
        model.objects.bulk_create(batch, batch_size)


class Command(BaseCommand):

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout, stderr, no_color, force_color)
        self.user_count = None
        self.tag_count = None
        self.question_count = None
        self.answer_count = None
        self.alike_count = None
        self.qlike_count = None

        self.user_ids = []
        self.f = Faker()

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=100)
        parser.add_argument('--tags', type=int, default=100)
        parser.add_argument('--questions', type=int, default=100)
        parser.add_argument('--answers', type=int, default=100)
        parser.add_argument('--qlikes', type=int, default=100)
        parser.add_argument('--alikes', type=int, default=100)

    def handle(self, *args, **options):
        clear()
        self.user_count = options['users']
        self.tag_count = options['tags']
        self.question_count = options['questions']
        self.answer_count = options['answers']
        self.alike_count = options['alikes']
        self.qlike_count = options['qlikes']

        get_user_model().objects.create_superuser('admin', '', 'password')
        get_user_model().objects.create_user('user', '', 'xxx')
        self.create_users()
        self.create_tags()
        self.create_questions()
        self.create_answers()
        self.create_answer_likes()
        self.create_question_likes()

    def create_users(self):
        print(self.user_count, "Users")
        users = (User(username=''.join(self.f.words(4)), email=self.f.email(),
                      first_name=self.f.first_name(), password=self.f.password()) for _ in range(self.user_count))
        save_bulk(1000, users, User)
        self.user_ids = list(User.objects.values_list('id', flat=True))
        profiles = (Profile(user_id=self.user_ids[i]
                            ) for i in range(self.user_count))
        save_bulk(1000, profiles, Profile)

    def create_tags(self):
        print(self.tag_count, "Tags")
        tags = (Tag(title=self.f.word() + '_' + self.f.word()) for _ in range(self.tag_count))
        save_bulk(1000, tags, Tag)

    def create_questions(self):
        print(self.question_count, "Questions")
        tag_ids = list(Tag.objects.values_list('id', flat=True))
        questions = (Question(user_id=choice(self.user_ids),
                              title=self.f.sentence(),
                              text=self.f.text(max_nb_chars=2000),
                              ) for _ in range(self.question_count))
        save_bulk(100, questions, Question)
        print('meh')
        questions = Question.objects.all()
        for question in questions:
            question.tags.add(*sample(tag_ids, randint(1, 5)))
        # Question.objects.bulk_update(questions, ['tags'])

    def create_answers(self):
        print(self.answer_count, "Answers")
        question_ids = list(Question.objects.values_list('id', flat=True))
        answers = (Answer(user_id=choice(self.user_ids),
                          question_id=choice(question_ids),
                          text=self.f.text(max_nb_chars=1000)
                          ) for _ in range(self.answer_count))
        save_bulk(1000, answers, Answer)
        questions = Question.objects.all()
        for question in questions:
            question.answer_count = Answer.objects.by_question(question.id).count()
        Question.objects.bulk_update(questions, ['answer_count'])

    def create_answer_likes(self):
        print(self.alike_count, "Answer likes")
        answer_ids = list(Answer.objects.values_list('id', flat=True))
        likes = (AnswerLike(user_id=choice(self.user_ids),
                            answer_id=choice(answer_ids),
                            is_upvote=self.f.boolean()
                            ) for _ in range(self.alike_count))
        save_bulk(1000, likes, AnswerLike)
        print("Saved, computing answers")
        answers = Answer.objects.all()
        for i in range(len(answers)):
            answers[i].like_count = AnswerLike.objects.ans_upvotes(answers[i].id).count() - \
                                    AnswerLike.objects.ans_downvotes(answers[i].id).count()
        Answer.objects.bulk_update(answers, ['like_count'])

    def create_question_likes(self):
        print(self.alike_count, "Question likes")
        question_ids = list(Question.objects.values_list('id', flat=True))
        likes = (QuestionLike(user_id=choice(self.user_ids),
                              question_id=choice(question_ids),
                              is_upvote=self.f.boolean()
                              ) for _ in range(self.qlike_count))

        save_bulk(1000, likes, QuestionLike)
        print("Saved, computing questions")
        questions = Question.objects.all()
        for i in range(len(questions)):
            questions[i].like_count = QuestionLike.objects.q_upvotes(questions[i].id).count() - \
                                      QuestionLike.objects.q_downvotes(questions[i].id).count()
        Question.objects.bulk_update(questions, ['like_count'])
