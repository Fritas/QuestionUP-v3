"""
    Instancia o bd para o sistema flask
"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from . import db, login_manager

class Permissao:
    JOGAR = 1
    MODERADOR = 8
    ADMIN = 16

class Grupo(db.Model):
    __tablename__ = 'grupo'
    cod_grupo = db.Column(db.Integer, primary_key=True)
    grupo_nome = db.Column(db.String(64), unique=True)
    grupo_padrao = db.Column(db.Boolean, default=False, index=True)
    permissoes = db.Column(db.Integer)
    usuarios = db.RelationshipProperty('Usuario', backref='grupo', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Grupo, self).__init__(**kwargs)
        if self.permissoes is None:
            self.permissoes = 0

    @staticmethod
    def inserir_grupos():
        grupos = {
            'Usuario': [Permissao.JOGAR],
            'Moderador': [Permissao.JOGAR, Permissao.MODERADOR],
            'Administrador': [Permissao.JOGAR, Permissao.MODERADOR, Permissao.ADMIN],
        }
        grupo_padrao = 'Usuario'
        for g in grupos:
            grupo = Grupo.query.filter_by(grupo_nome=g).first()
            if grupo is None:
                grupo = Grupo(name=g)
            grupo.resetar_permissoes()
            for perm in grupos[g]:
                grupo.adicionar_permissao(perm)
            grupo.grupo_padrao = (grupo.grupo_nome == grupo_padrao)
            db.session.add(grupo)
        db.session.commit()

    def adicionar_permissao(self, perm):
        if not self.tem_permissao(perm):
            self.permissoes += perm

    def remover_permissao(self, perm):
        if self.tem_permissao(perm):
            self.permissoes -= perm

    def resetar_permissoes(self):
        self.permissoes = 0

    def tem_permissao(self, perm):
        return self.permissoes & perm == perm

    def __repr__(self):
        return '<Grupo %r>' %self.grupo_nome

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuario'
    cod_usuario = db.Column(db.Integer, primary_key=True)
    cod_grupo = db.Column(db.Integer, db.ForeignKey('grupo.cod_grupo'))
    usuario = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    senha_hash = db.Column(db.String(128))
    questoes_acertadas = db.Column(db.Integer, nullable=False)
    membro_desde = db.Column(db.DateTime(), default=datetime.utcnow)
    questoes = db.RelationshipProperty('Questao', backref='usuario', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Usuario, self).__init__(**kwargs)
        if self.grupo is None:
            if self.grupo is None:
                self.grupo = Grupo.query.filter_by(grupo_padrao=True).first()

    @property
    def senha(self):
        raise AttributeError('não é possível fazer a leitura desse atributo')

    @senha.setter
    def senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def pode_fazer(self, perm):
        return self.grupo is not None and self.grupo.tem_permissao(perm)

    def is_administrator(self):
        return self.pode_fazer(Permissao.ADMIN)

class UsuarioAnonimo(AnonymousUserMixin):
    def pode_fazer(self, permissoes):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = UsuarioAnonimo

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))