"""
    Instancia formularios flask para a aplicacao principal
"""

from flask_wtf import FlaskForm
from wtforms import SubmitField

class ConfirmarRepostaForm(FlaskForm):
    enviar = SubmitField('Confirmar')