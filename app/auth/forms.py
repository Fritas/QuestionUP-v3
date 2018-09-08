"""
    Instancia formularios flask para a aplicacao de autenticacao
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp
from ..models import Usuario

class LoginForm(FlaskForm):
    usuario = StringField('Usuário', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    enviar = SubmitField('Entrar')

class RegistrarForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email('Endereço de email inválido.')])
    usuario = StringField('Usuário', validators=[DataRequired(), Length(1, 64),
                                                 Regexp('^[A-Za-z][A-Za-z0-9]*$', 0,
                                                        'Nomes de usuários podem ter '
                                                        'somente letras e números ')])
    senha = PasswordField('Senha', validators=[DataRequired(), EqualTo('senha2', message='Senhas precisam ser iguais.')])
    senha2 = PasswordField('Confirmar senha', validators=[DataRequired()])
    enviar = SubmitField('Registrar-se')

    def validar_email(self, email):
        if Usuario.query.filter_by(email=email.data).first():
            raise ValidationError('Email já cadastrado.')

    def validar_usuario(self, usuario):
        if Usuario.query.filter_by(usuario=usuario.data).first():
            raise ValidationError('Usuário em uso.')