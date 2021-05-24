# Created by @daguilarm at 24/5/21

from orator.migrations import Migration


class CreateUsersTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('users') as table:
            table.big_increments('id')
            table.char('name', 150)
            table.char('surname', 150)
            table.char('email', 150)
            table.char('telephone', 15)
            table.text('address')
            table.char('city', 150)
            table.char('state', 150)
            table.char('country', 150).default('España')
            table.char('role', 10)
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('users')
