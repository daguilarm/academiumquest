# Columns
columns = {
    # Table labels
    'headers': [
        'ID',
        'Usuario',
        'Asignatura',
        'Preguntas',
        'Respuesta 1',
        'Respuesta 2',
        'Respuesta 3',
        'Respuesta 4',
        'Correcta',
        'Tipo',
        'Utilizada en...'
    ],
    # Database table columns
    'columns': [
        'id',
        'user',
        'category',
        'question',
        'answer_1',
        'answer_2',
        'answer_3',
        'answer_4',
        'correct',
        'type',
        'used'
    ],
    # Width in %
    'width': ['2', '5', '4', '40', '9', '9', '9', '9', '4', '4', '5'],
}

# Database defaults
database = {
    'per_page': 10,
    'page': 1,
    'order': 'id',
    'direction': 'ASC',
    'filter': {},
}

# Emtpy results
empty_results = '┄'
