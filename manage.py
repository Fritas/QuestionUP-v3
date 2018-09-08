"""
    Gerencia outras funcoes do sistema (Nada no momento)
"""

import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

from flask_migrate import Migrate
from app import create_app, db


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

app.run()