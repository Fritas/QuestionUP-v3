"""
    Controller da aplicacao principal
"""

from flask import render_template, flash, redirect, url_for
#from flask_login import login_required
from . import main
from .forms import QuestaoJogoForm
from ..models import Questao

@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@main.route('/jogar', methods=['GET', 'POST'])
def jogar():
    form = QuestaoJogoForm()
    if form.validate_on_submit():
        questao = Questao.query.filter_by(cod_questao=form.cod_questao.data).first()
        print(form.questao.data)
        if questao is not None and questao.verificar_resposta(form.questao.data):
            return redirect(url_for('main.jogar'))
        flash('Questão inválida.')
    return render_template('jogar.html', form=form)

@main.route('/ranking')
def ranking():
    return '<__MAIN__> RANKING'