# Created by @daguilarm at 24/5/21
import orator
from orator import DatabaseManager

databases = {
    'sqlite': {
        'driver': 'sqlite',
        'database': './database/sqlite.db',
        'prefix': '',
    }
}

db = DatabaseManager(databases)


# Get the table categories
def categories():
    return db.table('categories').select('name').get()


# Get the table results
def questions(db_total_pages, db_page, db_order_by, db_direction, db_filter):

    query = db.\
        table('questions').\
        join('categories', 'categories.id', '=', 'questions.category_id').\
        join('users', 'users.id', '=', 'questions.user_id').\
        select(
            'questions.id AS id',
            'users.name AS user',
            'categories.name AS category',
            'questions.question AS question',
            'questions.answer_1 AS answer_1',
            'questions.answer_2 AS answer_2',
            'questions.answer_3 AS answer_3',
            'questions.answer_4 AS answer_4',
            'questions.correct AS correct',
            'questions.type AS type',
            'questions.used_at AS used',
        ).\
        order_by(db_order_by, db_direction)

    # Multiple filter [type, category]
    if db_filter:
        for key, value in db_filter.items():
            if key and value:
                query = query.\
                    where(key, '=', value)

    return query.paginate(db_total_pages, db_page)
