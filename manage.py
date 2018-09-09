"""
    Gerencia outras funcoes do sistema (Nada no momento)
"""

#!/usr/bin/env python
import os

COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

if os.path.exists('.env'):
    print('Importando ambiente virtual de .env...')
    for linha in open('.env'):
        var = linha.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

from app import create_app, db
from app.models import Usuario, Grupo, Categoria, Questao
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, Usuario=Usuario, Grupo=Grupo, Categoria=Categoria, Questao=Questao)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def test(coverage=False):
    """ Executar unidades de testes """
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Resumo do Coverage:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('Versão HTML: file://%s/index.html' %covdir)
        COV.erase()

@manager.command
def perfil(tamanho=25, dir_perfil=None):
    """ Iniciar a aplicacao atraves do codigo de perfil """
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[tamanho], profile_dir=dir_perfil)
    app.run()

@manager.command
def montar():
    """ Executar processo de montagem """
    from flask_migrate import upgrade
    from app.models import Grupo

    # migrar db para revisao final
    upgrade()

    # criar grupos de usuarios (usuario, mod, admin)
    Grupo.inserir_grupos()

if __name__ == '__main__':
    manager.run()