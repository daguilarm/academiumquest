# Created by @daguilarm at 24/5/21
from orator.migrations import Migration


class CreateQuestionsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('questions') as table:
            table.big_increments('id')
            table.integer('user_id').unsigned()
            table.foreign('user_id').references('id').on('users')
            table.text('question')
            table.text('answers')
            table.char('correct', 1)
            table.char('type', 3)
            table.timestamp('used_at')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('questions')
