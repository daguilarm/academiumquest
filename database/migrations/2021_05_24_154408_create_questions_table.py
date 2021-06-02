# Created by @daguilarm at 24/5/21
from orator.migrations import Migration


class CreateQuestionsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('questions') as table:
            table.big_increments('id')
            table.integer('user_id').unsigned().index()
            table.integer('category_id').unsigned().index()
            table.text('question')
            table.text('notes')
            table.text('answer_1')
            table.text('answer_2')
            table.text('answer_3')
            table.text('answer_4')
            table.text('answer_5')
            table.char('correct', 1)
            table.char('type', 3)
            table.timestamp('used_at')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('questions')
