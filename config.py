# Columns
columns = {
    'headers': ['ID', 'Usuario', 'Categoría', 'Preguntas', 'Respuesta 1', 'Respuesta 2', 'Respuesta 3', 'Respuesta 4',
                'Correcta', 'Tipo', 'Utilizada en...'],
    'columns': ['id', 'user', 'category', 'question', 'answer_1', 'answer_2', 'answer_3', 'answer_4', 'correct', 'type',
                'used'],
    # Width in %
    'width': ['1', '5', '5', '40', '10', '10', '10', '10', '2', '2', '4'],
}

# Data base
database = {
    'per_page': 10,
    'page': 0,
    'order': 'questions.id',
    'direction': 'ASC'
}