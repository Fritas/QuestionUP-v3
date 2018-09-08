"""
    Controller da aplicacao de autenticacao
"""

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..models import Usuario
from .forms import LoginForm, RegistrarForm

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(usuario=form.usuario.data).first()
        if usuario is not None and usuario.verificar_senha(form.senha.data):
            login_user(usuario)
            return redirect(url_for('main.index'))
        flash('Usuario ou senha inválidos.')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você desconectou-se da conta.')
    return redirect(url_for('main.index'))

@auth.route('/registrar', methods=['GET', 'POST'])
def registrar():
    form = RegistrarForm()
    if form.validate_on_submit():
        usuario = Usuario(email=form.email.data,
                          usuario=form.usuario.data,
                          senha=form.senha.data)
        db.session.add(usuario)
        db.session.commit()
        flash('Você foi cadastrado ao QuestionUP!')
        return redirect(url_for('auth.login'))
    return render_template('auth/registrar.html', form=form)