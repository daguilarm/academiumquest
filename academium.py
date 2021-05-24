# Created by @daguilarm at 24/5/21

import tkinter


# Create the table
def db_migrate():
    from database import migration
    migration.db_create()


# Populate table
def db_seeder():
    from database.seeds import db_seed
    db_seed()


db_seeder()
