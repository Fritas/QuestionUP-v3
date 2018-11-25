"""
    Controller da aplicacao de autenticacao
"""

from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user, logout_user, login_required
from . import auth
from .. import db
from ..models import Usuario
from .forms import LoginForm, RegistrarForm

@auth.route('/login', methods=['GET', 'POST'])
def login():
    try:
        form = LoginForm()
        if form.validate_on_submit():
            usuario = Usuario.query.filter_by(usuario=form.usuario.data).first()
            if usuario is not None and usuario.verificar_senha(form.senha.data):
                login_user(usuario)
                next = request.args.get('next')
                if next is None or not next.startswith('/'):
                    next = url_for('main.index')
                return redirect(next)
            flash('Usuario ou senha inválidos.')
        return render_template('auth/login.html', form=form)
    except Exception as e:
        abort(500, e)

@auth.route('/logout')
@login_required
def logout():
    try:
        logout_user()
        flash('Você desconectou-se da conta.')
        return redirect(url_for('main.index'))
    except Exception as e:
        abort(500, e)

@auth.route('/registrar', methods=['GET', 'POST'])
def registrar():
    try:
        form = RegistrarForm()
        if form.validate_on_submit():
            usuario = Usuario(email=form.email.data,
                            usuario=form.usuario.data,
                            senha=form.senha.data,
                            cod_grupo=0)
            db.session.add(usuario)
            db.session.commit()
            flash('Você foi cadastrado ao QuestionUP!')
            login_user(usuario)
            return redirect(url_for('main.index'))
        return render_template('auth/registrar.html', form=form)
    except Exception as e:
        abort(500, e)