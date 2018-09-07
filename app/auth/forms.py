"""
    Instancia formularios flask para a aplicacao de autenticacao
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    usuario = StringField('nom_usuario', validators=[DataRequired()])
    senha = PasswordField('den_senha', validators=[DataRequired()])
    enviar = SubmitField('Entrar')

