# Columns
columns = {
    'headers': ['ID', 'Usuario', 'Categoría', 'Preguntas', 'Respuesta 1', 'Respuesta 2', 'Respuesta 3', 'Respuesta 4',
                'Correcta', 'Tipo', 'Utilizada en...'],
    'columns': ['id', 'user', 'category', 'question', 'answer_1', 'answer_2', 'answer_3', 'answer_4', 'correct', 'type',
                'used'],
    # Width in %
    'width': ['2', '5', '4', '40', '9', '9', '9', '9', '4', '4', '5'],
}

# Data base
database = {
    'per_page': 10,
    'page': 1,
    'order': 'questions.id',
    'direction': 'ASC'
}