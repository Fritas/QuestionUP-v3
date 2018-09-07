"""
    Controller da aplicacao de autenticacao
"""

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import Usuario
from .forms import LoginForm

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