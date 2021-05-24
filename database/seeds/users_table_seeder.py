# Created by @daguilarm at 24/5/21
from orator.seeds import Seeder


class UsersTableSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        self.db.table('users').insert({
            'name': 'Paula Maria',
            'surname': 'Aguilar Morales',
            'email': 'paulan@aguilar.com',
            'telephone': '+34 000 000 000',
            'address': 'C/ Sin nombre 10',
            'city': 'San Javier',
            'state': 'Murcia',
            'country': 'España',
            'role': 'user'
        })
