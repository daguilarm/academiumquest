# Created by @daguilarm at 24/5/21
from faker import Faker
from orator.seeds import Seeder
import json
import random

fake = Faker()


class QuestionsTableSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        for i in range(100):
            with_insert(self, i)


def with_insert(self, i):
    """
    Run the database seeds.
    """
    self.db.table('questions').insert({
        'user_id': 1,
        'category_id': random_number(1, 4),
        'question': fake.paragraph(nb_sentences=10),
        'answers': random_answer(),
        'correct': random_number(1, 4),
        'type': random_type(),
        'used_at': random_date(),
    })


def random_answer():
    result = [
        fake.paragraph(nb_sentences=2),
        fake.paragraph(nb_sentences=3),
        fake.paragraph(nb_sentences=2),
        fake.paragraph(nb_sentences=4)
    ]
    return json.dumps(result)


def random_number(start, end):
    return random.randint(start, end)


def random_date():
    foo = ('null', fake.date_this_month().strftime("%Y-%m-%d %H:%M:%S"))
    return random.choice(foo)


def random_type():
    foo = ('eir', 'ope')
    return random.choice(foo)
