# Created by @daguilarm at 24/5/21
from orator import DatabaseManager

databases = {
    'sqlite': {
        'driver': 'sqlite',
        'database': './database/sqlite.db',
        'prefix': '',
    }
}

db = DatabaseManager(databases)


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
                # Used filter
                if key == 'used' and value == 'used_at_null':
                    query = query.\
                        where('questions.used_at', '=', '')
                # Used filter
                elif key == 'category':
                    query = query.\
                        where('questions.category_id', '=', value)
                # Rest of the filters
                else:
                    query = query.\
                        where(key, '=', value)
    # Debug
    # print(query.to_sql())
    return query.paginate(db_total_pages, db_page)

# Update questions
def questions_update(fields):
    return db.\
        table('questions').\
        where('id', fields.get('id')).\
        update(
        {
            'category_id': fields.get('category'),
            'question': fields.get('question'),
            'answer_1': fields.get('answer_1'),
            'answer_2': fields.get('answer_2'),
            'answer_3': fields.get('answer_3'),
            'answer_4': fields.get('answer_4'),
            'correct': fields.get('correct'),
            'type': fields.get('type'),
        }
    )

# Get all the categories
def categories():
    return db.\
        table('categories').\
        select('id', 'name').\
        order_by('name').\
        get()
