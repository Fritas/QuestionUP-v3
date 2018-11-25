"""
    Controller da aplicacao principal
    Separado para erros de excecoes da web
"""

from . import main
from flask import render_template

@main.app_errorhandler(404)
def page_not_found(e):
    return '<center>Página não encontrada!</br>%s</center>' %(e)

@main.app_errorhandler(500)
def erro_interno(e):
    return render_template('e500.html', e=e)