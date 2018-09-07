"""
    Controller da aplicacao principal
    Separado para erros de excecoes da web
"""

from . import main

@main.app_errorhandler(404)
def page_not_found(e):
    return '<center>Página não encontrada!</br>%s</center>' %(e)
