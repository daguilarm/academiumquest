# Created by @daguilarm at 24/5/21
from faker import Faker
from orator.seeds import Seeder

fake = Faker()


class CategoriesTableSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        for i in range(10):
            with_insert(self, i)


def with_insert(self, i):
    """
    Run the database seeds.
    """
    self.db.table('categories').insert({
        'name': fake.name(),
        'description': fake.paragraph(nb_sentences=3),
    })
