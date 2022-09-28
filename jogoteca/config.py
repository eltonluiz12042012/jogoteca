import os

SECRET_KEY = 'LiviaFragadoFranco'
#SQLALCHEMY_TRACK_MODIFICATIONS = False

SQLALCHEMY_DATABASE_URI = \
    '{SGDB}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGDB='mysql+mysqlconnector',
        usuario='root',
        senha='root',
        servidor='localhost',
        database='jogoteca'
    )

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'