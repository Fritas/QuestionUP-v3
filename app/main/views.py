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
    try:
        if lista_questoes == []:
            lista_questoes.append(None)
            abort(500)
        if lista_questoes[0] == None:
            try:
                lista_questoes.clear()
                questoes = Questao.query.all()
                for questao in questoes:
                    lista_questoes.append(questao)
            except IndexError:
                return index()
        numero_aleatorio = random.randrange(0, len(lista_questoes))
        return lista_questoes[numero_aleatorio]
    except:
        abort(500)

def questao_sequencial(codigo_questao):
    questao = Questao.query.filter_by(cod_questao=codigo_questao).first()
    return questao

def getQuestao(cod_questao):
    questao = Questao.query.filter_by(cod_questao=cod_questao).first()
    existe = db.session.query(db.exists().where(Questao.cod_questao == cod_questao)).scalar()
    if not existe:
        abort(500)
    return questao

@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@main.route('/jogar', methods=['GET', 'POST'])
@login_required
def jogar():
    try:
        if request.method == 'GET':
            questao = questao_aleatoria() #se for aleatorio, tirar comentario dessa linha
            #questao = getQuestao(1) # se for aleatorio, remover essa linha
            form = ConfirmarRepostaForm()
            return render_template('jogar.html', questao=questao, form=form)
        if request.method == 'POST':
            usuario = Usuario.query.filter(Usuario.cod_usuario == str(current_user.cod_usuario)).first()
            alternativa_escolhida = request.form['questao']
            cod_questao = request.form['cod_questao']
            questao = getQuestao(cod_questao)
            if verificar_resposta(questao, alternativa_escolhida):
                questao = questao_aleatoria() # se for aleatorio, tirar comentario dessa linha
                #cod = int(cod_questao) # se for aleatorio, remover essa linha
                #cod += 1 # se for aleatorio, remover essa linha
                #questao = getQuestao(cod) # se for aleatorio, mudar cod para cod_questao
                questao = getQuestao(questao)
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
    except:
        abort(500)

@main.route('/ranking')
def ranking():
    try:
        p = request.args.get('p')
        if request.args.get('p') == None:
            p = '1'
        ppage = int(p)
        usuarios = Usuario.query.order_by(Usuario.questoes_acertadas.desc(),Usuario.numero_jogos.asc(),Usuario.usuario.asc()).paginate(per_page=10, page=ppage, error_out=True)
        return render_template('ranking.html', usuarios=usuarios, pp = ppage)
    except:
        abort(500)