"""
    Controller da aplicacao de administracao
"""

from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from . import admin
from .forms import InserirQuestaoForm, InserirCategoriaForm
from .. import db
from ..models import Usuario, Questao, Categoria

@admin.route('/')
@login_required
def index():
    """ Abre pagina 'ponte' que interliga todas as paginas com fins administrativos """
    if current_user.is_administrator():
        return render_template('admin/index.html')
    return redirect(url_for('main.index'))

@admin.route('/inserir_questao', methods=['GET', 'POST'])
@login_required
def inserir_questao():
    """ Abre pagina com formulario para adicionar nova questao ao sistema """
    if current_user.is_administrator():
        form = InserirQuestaoForm()
        if form.validate_on_submit():
            questao = Questao(
                cod_categoria=form.cod_categoria.data,
                cod_usuario=current_user.cod_usuario,
                questao=form.questao.data,
                alternativa1=form.alternativa1.data,
                alternativa2=form.alternativa2.data,
                alternativa3=form.alternativa3.data,
                alternativa4=form.alternativa4.data,
                alternativa5=form.alternativa5.data,
                alternativa_correta=form.alternativa_correta.data
            )
            db.session.add(questao)
            db.session.commit()
            return redirect(url_for('admin.inserir_questao'))
        return render_template('admin/inserir_questao.html', form=form)
    return redirect(url_for('main.index'))

@admin.route('/inserir_categoria', methods=['GET', 'POST'])
@login_required
def inserir_categoria():
    """ Abre pagina com formulario para adicionar nova categoria ao sistema """
    if current_user.is_administrator():
        form = InserirCategoriaForm()
        if form.validate_on_submit():
            categoria = Categoria(
                categoria_nome=form.categoria_nome,
            )
            db.session.add(categoria)
            db.session.commit()
            return redirect(url_for('admin.inserir_categoria'))
        return render_template('admin/inserir_categoria.html', form=form)
    return redirect(url_for('main.index'))