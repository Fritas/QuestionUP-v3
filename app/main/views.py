"""
    Controller da aplicacao principal
"""

import random
from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import login_required, current_user
from . import main
from .forms import ConfirmarRepostaForm
from .. import db
from ..models import Questao, Usuario

numero_acertos = 0

def verificar_resposta(questao, resposta):
    if questao.alternativa_correta == resposta:
        return True
    return False

def questao_aleatoria():
    qtd_questoes_disponiveis = random.randrange(0, Questao.query.count())
    questao = Questao.query[qtd_questoes_disponiveis]
    return questao

def getQuestao(cod_questao):
    questao = Questao.query.filter_by(cod_questao=cod_questao).first()
    return questao

@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@main.route('/jogar', methods=['GET', 'POST'])
@login_required
def jogar():
    try:
        if request.method == 'GET':
            questao = questao_aleatoria()
            form = ConfirmarRepostaForm()
            return render_template('jogar.html', questao=questao, form=form)
        if request.method == 'POST':
            usuario = Usuario.query.filter(Usuario.cod_usuario == str(current_user.cod_usuario)).first()
            alternativa_escolhida = request.form['questao']
            cod_questao = request.form['cod_questao']
            questao = getQuestao(cod_questao)
            if verificar_resposta(questao, alternativa_escolhida):
                questao = questao_aleatoria()
                form = ConfirmarRepostaForm()
                global numero_acertos
                numero_acertos += 1
                if numero_acertos > usuario.questoes_acertadas:
                    usuario.questoes_acertadas = numero_acertos
                db.session.commit()
                flash('Parabéns, você acertou mais uma questão!')
                return redirect(url_for('main.jogar', questao=questao, form=form))
            numero_acertos = 0
            usuario.numero_jogos = usuario.numero_jogos + 1
            db.session.commit()
            flash('Que pena! Você errou, com isso seu placar foi a zero!')
            return redirect(url_for('main.ranking'))
    except Exception:
        abort(500)

@main.route('/ranking')
def ranking():
    usuarios = Usuario.query.order_by(Usuario.questoes_acertadas.desc()).all()
    #pagination = Pagination(total=usuarios.count(), record_name='usuarios')
    return render_template('ranking.html', usuarios=usuarios)#, pagination=pagination)