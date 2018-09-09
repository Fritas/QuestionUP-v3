"""
    Instancia o bd para o sistema flask
"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from . import db, login_manager


class Grupo(db.Model):
    __tablename__ = 'grupos'
    cod_grupo = db.Column(db.Integer, primary_key=True)
    grupo_nome = db.Column(db.String(64), unique=True)
    usuarios = db.RelationshipProperty('Usuario', backref='grupos', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Grupo, self).__init__(**kwargs)

    def __repr__(self):
        return '<Grupo %r>' %self.grupo_nome

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    cod_usuario = db.Column(db.Integer, primary_key=True)
    cod_grupo = db.Column(db.Integer, db.ForeignKey('grupos.cod_grupo'))
    usuario = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    senha_hash = db.Column(db.String(128))
    questoes_acertadas = db.Column(db.Integer, nullable=False)
    numero_jogos = db.Column(db.Integer, nullable=False)
    membro_desde = db.Column(db.DateTime(), default=datetime.utcnow)
    questoes = db.RelationshipProperty('Questao', backref='usuarios', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Usuario, self).__init__(**kwargs)
        self.questoes_acertadas = 0
        self.numero_jogos = 0

    @property
    def senha(self):
        raise AttributeError('não é possível fazer a leitura desse atributo')

    @senha.setter
    def senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def is_administrator(self):
        """ Verifica se a pessoa eh admin(id=1) ou usuario(id=0) """
        if self.cod_grupo == 1:
            return True
        return False

    def get_id(self):
        return self.cod_usuario

class UsuarioAnonimo(AnonymousUserMixin):
    def pode_fazer(self, permissoes):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = UsuarioAnonimo

@login_manager.user_loader
def load_user(cod_usuario):
    return Usuario.query.get(int(cod_usuario))

class Questao(db.Model):
    __tablename__ = 'questoes'
    cod_questao = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cod_categoria = db.Column(db.Integer, db.ForeignKey('categorias.cod_categoria'))
    cod_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.cod_usuario'))
    questao = db.Column(db.String(512), nullable=False)
    alternativa1 = db.Column(db.String(256), nullable=False)
    alternativa2 = db.Column(db.String(256), nullable=False)
    alternativa3 = db.Column(db.String(256), nullable=False)
    alternativa4 = db.Column(db.String(256), nullable=False)
    alternativa5 = db.Column(db.String(256), nullable=True)
    alternativa_correta = db.Column(db.String(15), nullable=False)

    def __init__(self, **kwargs):
        super(Questao, self).__init__(**kwargs)

    @staticmethod
    def pegar_questao_aleatoria():
        pass

class Categoria(db.Model):
    __tablename__ = 'categorias'
    cod_categoria = db.Column(db.Integer, primary_key=True, autoincrement=True)
    categoria_nome = db.Column(db.String(32), unique=True)
    questoes = db.RelationshipProperty('Questao', backref='categorias', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Categoria, self).__init__(**kwargs)