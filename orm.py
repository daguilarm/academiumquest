# Created by @daguilarm at 24/5/21
from orator import DatabaseManager

databases = {
    'sqlite': {
        'driver': 'sqlite',
        'database': './database/sqlite.db',
        'prefix': ''
    }
}

db = DatabaseManager(databases)


# Get the table results
def orm_results():
    return db.\
        table('questions').\
        join('categories', 'categories.id', '=', 'questions.category_id').\
        join('users', 'users.id', '=', 'questions.user_id').\
        select(
            'questions.id AS id',
            'questions.question AS question',
            'questions.answers AS answers',
            'questions.correct AS correct',
            'questions.type AS type',
            'questions.used_at AS used',
            'categories.name AS category',
            'users.name AS user',
        ).get()
