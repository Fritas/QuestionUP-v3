"""
    Controller da aplicacao principal
"""

import random
from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import login_required, current_user
from sqlalchemy.sql import exists
from . import main
from .forms import ConfirmarRepostaForm
from .. import db
from ..models import Questao, Usuario

numero_acertos = 0
#nr_codigo = 1
lista_questoes = [None]

def verificar_resposta(questao, resposta):
    if questao.alternativa_correta == resposta:
        return True
    return False

def questao_aleatoria():
    if lista_questoes == []:
        lista_questoes.append(None)
        abort(500)
    if lista_questoes[0] == None:
        lista_questoes.clear()
        questoes = Questao.query.all()
        for questao in questoes:
            lista_questoes.append(questao)
    numero_aleatorio = random.randrange(0, len(lista_questoes))
    print(lista_questoes)
    return lista_questoes[numero_aleatorio]

def questao_sequencial(codigo_questao):
    questao = Questao.query.filter_by(cod_questao=codigo_questao).first()
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
    if request.method == 'GET':
        questao = questao_aleatoria()
        #global nr_codigo
        #questao = questao_sequencial(nr_codigo)
        form = ConfirmarRepostaForm()
        return render_template('jogar.html', questao=questao, form=form)
    if request.method == 'POST':
        usuario = Usuario.query.filter(Usuario.cod_usuario == str(current_user.cod_usuario)).first()
        alternativa_escolhida = request.form['questao']
        cod_questao = request.form['cod_questao']
        questao = getQuestao(cod_questao)
        print(lista_questoes)
        if verificar_resposta(questao, alternativa_escolhida):
            #lista_questoes.remove(questao)
            questao = questao_aleatoria()
            #if db.session.query.exists().where(Questao.cod_questao=nr_codigo+1).scalar()
             #   nr_codigo += 1
            #questao = questao_sequencial(nr_codigo)
            form = ConfirmarRepostaForm()
            global numero_acertos
            numero_acertos += 1
            if numero_acertos > usuario.questoes_acertadas:
                usuario.questoes_acertadas = numero_acertos
            db.session.commit()
            flash('Parabéns, você acertou mais uma questão!')
            return render_template('jogar.html', questao=questao, form=form)
        numero_acertos = 0
        usuario.numero_jogos = usuario.numero_jogos + 1
        db.session.commit()
        lista_questoes[0] = None
        flash('Que pena! Você errou, com isso seu placar foi a zero!')
        return redirect(url_for('main.ranking'))

@main.route('/ranking')
def ranking():
    usuarios = Usuario.query.order_by(Usuario.questoes_acertadas.desc()).all()
    #pagination = Pagination(total=usuarios.count(), record_name='usuarios')
    return render_template('ranking.html', usuarios=usuarios)#, pagination=pagination)