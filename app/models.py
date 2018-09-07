"""
    Instancia o bd para o sistema flask
"""

from datetime import datetime
from . import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.cod_user

