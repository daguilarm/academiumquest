# Created by @daguilarm at 24/5/21
from orator import DatabaseManager, Schema

databases = {
    'sqlite': {
        'driver': 'sqlite',
        'database': './database/sqlite.db',
        'prefix': ''
    }
}

db = DatabaseManager(databases)
schema = Schema(db)
