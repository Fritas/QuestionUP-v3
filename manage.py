"""
    Gerencia outras funcoes do sistema (Nada no momento)
"""

import os
from app import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app.run()