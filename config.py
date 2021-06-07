"""
    All the configuration variables
"""

# Columns
columns = {
    # Table labels
    'headers': [
        'ID',
        'Tema',
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
    'width': ['2', '6', '40', '10', '10', '10', '10', '4', '3', '5'],
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
