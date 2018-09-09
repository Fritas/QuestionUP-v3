"""
    Controller da aplicacao principal
    Separado para erros de excecoes da web
"""

from . import main

@main.app_errorhandler(404)
def page_not_found(e):
    return '<center>Página não encontrada!</br>%s</center>' %(e)

@main.app_errorhandler(500)
def nao_existem_questoes(e):
    return '<center><h1>ERRO 500</h1></br>Ops, algo aconteceu!</br>%s</br><a href=/>Clique aqui para voltar a página inicial.</a></center>' %(e)