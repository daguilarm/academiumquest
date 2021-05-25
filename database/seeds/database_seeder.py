# Created by @daguilarm at 24/5/21
from database.seeds.categories_table_seeder import CategoriesTableSeeder
from database.seeds.questions_table_seeder import QuestionsTableSeeder
from database.seeds.users_table_seeder import UsersTableSeeder
from orator.seeds import Seeder


class DatabaseSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        self.call(UsersTableSeeder)
        self.call(QuestionsTableSeeder)
        self.call(CategoriesTableSeeder)
