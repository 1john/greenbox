import dj_database_url
import os

os.environ['DATABASE_URL'] = 'postgres://postgres:postgres@localhost:5432/gbbdb'