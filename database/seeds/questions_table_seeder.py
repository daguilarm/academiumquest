# Created by @daguilarm at 24/5/21
from faker import Faker
from orator.seeds import Seeder
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
        'notes': fake.paragraph(nb_sentences=4),
        'answer_1': fake.paragraph(nb_sentences=2),
        'answer_2': fake.paragraph(nb_sentences=1),
        'answer_3': fake.paragraph(nb_sentences=3),
        'answer_4': fake.paragraph(nb_sentences=2),
        'answer_5': fake.paragraph(nb_sentences=1),
        'correct': random_number(1, 4),
        'type': random_type(),
        'used_at': random_date(),
    })


def random_number(start, end):
    return random.randint(start, end)


def random_date():
    foo = ('', fake.date_this_month().strftime("%Y-%m-%d %H:%M:%S"))
    return random.choice(foo)


def random_type():
    foo = ('eir', 'ope')
    return random.choice(foo)
