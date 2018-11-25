"""
    Controller da aplicacao de administracao
"""

from flask import render_template, redirect, url_for, request, abort
from flask_login import login_required, current_user
from . import admin
from ..main.views import lista_questoes
from .forms import InserirQuestaoForm, InserirCategoriaForm, AtualizarUsuarioForm
from .. import db
from ..models import Usuario, Questao, Categoria, Grupo

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
    try:
        if current_user.is_administrator():
            categorias = Categoria.query.all()
            if request.method == 'POST':
                questao = Questao(
                    cod_categoria = request.form['categoria'],
                    cod_usuario = current_user.cod_usuario,
                    questao = request.form['questao'],
                    alternativa1 = request.form['alternativa1'],
                    alternativa2 = request.form['alternativa2'],
                    alternativa3 = request.form['alternativa3'],
                    alternativa4 = request.form['alternativa4'],
                    alternativa5 = request.form['alternativa5'],
                    alternativa_correta = request.form['resposta']
                )
                db.session.add(questao)
                db.session.commit()
                return listar_questoes()
            return render_template('admin/inserir_questao.html', categorias=categorias)
        return redirect(url_for('main.index'))
    except:
        abort(500)

@admin.route('/deletar_questao', methods=['GET', 'POST'])
@login_required
def deletar_questao():
    """ Deletar questões """
    try:
        if current_user.is_administrator():
            questoes = Questao.query.all()
            if request.method == 'GET':
                return render_template('admin/deletar_questao.html', questoes=questoes)
            if request.method == 'POST':
                cod_id = request.form['questaoForm']
                questao = Questao.query.filter(Questao.cod_questao == cod_id).delete()
                db.session.commit()
                lista_questoes.clear()
                return redirect(url_for('admin.deletar_questao'))
        return redirect(url_for('main.index'))
    except:
        abort(500)

@admin.route('/inserir_categoria', methods=['GET', 'POST'])
@login_required
def inserir_categoria():
    """ Abre pagina com formulario para adicionar nova categoria ao sistema """
    try:
        if current_user.is_administrator():
            if request.method == 'POST':
                categoria = Categoria(
                    categoria_nome = request.form['categoria']
                )
                db.session.add(categoria)
                db.session.commit()
                return listar_questoes()
            return render_template('admin/inserir_categoria.html')
        return redirect(url_for('main.index'))
    except:
        abort(500)

@admin.route('/excluir_categoria')
@login_required
def excluir_categoria():
    """ Excluir uma categoria com id especificada pela url """
    try:
        if current_user.is_administrator():
            cod_id = request.args.get('id')
            categoria = Categoria.query.filter_by(cod_categoria = cod_id).one()
            db.session.delete(categoria)
            db.session.commit()
            return listar_questoes()
        return redirect(url_for('admin.listar_questoes'))
    except:
        abort(500)

@admin.route('/atualizar_categoria', methods=['GET','POST'])
@login_required
def atualizar_categoria():
    """ Atualizar dados de uma categoria a partir do id especificado pela url """
    try:
        if current_user.is_administrator():
            cod_id = request.args.get('id')
            categoria = Categoria.query.filter_by(cod_categoria = cod_id).one()
            if request.method == 'POST':
                categoria.categoria_nome = request.form['categoria_nome']
                db.session.commit()
                return redirect(url_for('admin.listar_questoes'))
            return render_template('admin/atualizar_categoria.html', categoria=categoria)
        return redirect(url_for('main.index'))
    except:
        abort(500)

@admin.route('/atualizar_usuario', methods=['GET', 'POST'])
@login_required
def atualizar_usuario():
    """ Abre uma pagina com formulario para atualizar informacoes do usuario """
    try:
        if current_user.is_administrator():
            cod_id = request.args.get('id')
            usuario = Usuario.query.filter_by(cod_usuario = cod_id).one()
            grupos = Grupo.query.all()
            if request.method == 'POST':
                usuario.usuario = request.form['usuario']
                usuario.email = request.form['email']
                usuario.senha = request.form['senha']
                usuario.cod_grupo = request.form['tipo_usuario']
                db.session.commit()
                return redirect(url_for('admin.listar_usuarios'))
            return render_template('admin/atualizar_usuario.html', usuario=usuario, grupos=grupos)
        return redirect(url_for('main.index'))
    except:
        abort(500)

@admin.route('/listar_usuarios', methods=['GET','POST'])
@login_required
def listar_usuarios():
    """ Abre uma pagina que lista todos os usuarios do sistema """
    try:
        if current_user.is_administrator():
            u = request.args.get('u')
            if request.args.get('u') == None:
                u = 1 
            upage = int(u)
            usuarios = Usuario.query.paginate(per_page=5, page=upage, error_out=True)
            g = request.args.get('g')
            if request.args.get('g') == None:
                g = 1
            gpage = int(g)
            grupos = Grupo.query.paginate(per_page=4, page=gpage, error_out=True)
            return render_template('admin/listar_usuarios.html', usuarios=usuarios, grupos=grupos, up=upage, gp=gpage)
        return redirect(url_for('main.index'))
    except:
        abort(500)

@admin.route('/excluir_usuario')
@login_required
def excluir_usuario():
    """ Exclui um usuario com id especificado pela url """
    try:
        if current_user.is_administrator():
            cod_id = request.args.get('id')
            usuario = Usuario.query.filter_by(cod_usuario = cod_id).one()
            db.session.delete(usuario)
            db.session.commit()
            return listar_usuarios()
        return redirect(url_for('main.index'))
    except:
        abort(500)

@admin.route('/listar_questoes')
@login_required
def listar_questoes():
    """ Abre uma pagina que lista todas as questoes do sistema """
    try:
        if current_user.is_administrator():
            q = request.args.get('q')
            if request.args.get('q') == None:
                q = 1
            qpage = int(q)
            questoes = Questao.query.paginate(per_page=5, page=qpage, error_out=True)
            c = request.args.get('c')
            if request.args.get('c') == None:
                c = 1
            cpage = int(c)
            categorias = Categoria.query.paginate(per_page=4, page=cpage, error_out=True)
            return render_template('admin/listar_questoes.html', questoes=questoes, categorias=categorias, qp=qpage, cp=cpage)
        return redirect(url_for('main.index'))
    except:
        abort(500)

@admin.route('/atualizar_questao', methods=['GET','POST'])
@login_required
def atualizar_questao():
    """ Abre uma pagina com formulario com dados da questao especificada por id, permitindo edita-los """
    try:
        if current_user.is_administrator():
            cod_id = request.args.get('id')
            questao = Questao.query.filter_by(cod_questao = cod_id).one()
            categorias = Categoria.query.all()
            if request.method == 'POST':
                questao.questao = request.form['questao']
                questao.alternativa1 = request.form['alternativa1']
                questao.alternativa2 = request.form['alternativa2']
                questao.alternativa3 = request.form['alternativa3']
                questao.alternativa4 = request.form['alternativa4']
                questao.alternativa5 = request.form['alternativa5']
                questao.alternativa_correta = request.form['resposta']
                questao.cod_categoria = request.form['categoria']
                db.session.commit()
                return redirect(url_for('admin.listar_questoes'))
            return render_template('admin/atualizar_questao.html', questao=questao, categorias=categorias)
        return redirect(url_for('main.index'))
    except:
        abort(500)

@admin.route('/excluir_questao')
@login_required
def excluir_questao():
    """ Excluir uma questão com id especificado pela url """
    try:
        if current_user.is_administrator():
            cod_id = request.args.get('id')
            questao = Questao.query.filter_by(cod_questao = cod_id).one()
            db.session.delete(questao)
            db.session.commit()
            return listar_questoes()
        return redirect(url_for('main.index'))
    except:
        abort(500)

@admin.route('/inserir_grupo', methods=['GET','POST'])
@login_required
def inserir_grupo():
    """ Inserir um novo grupo de usuario ao sistema """
    try:
        if current_user.is_administrator():
            if request.method == 'POST':
                grupo = Grupo(
                    grupo_nome = request.form['grupo_nome']
                )
                db.session.add(grupo)
                db.session.commit()
                return listar_usuarios()
            return render_template('admin/inserir_grupo.html')
        return redirect(url_for('main.index'))
    except:
        abort(500)

@admin.route('/excluir_grupo')
@login_required
def excluir_grupo():
    """ Excluir um grupo de usuario especificado pela url """
    try:
        if current_user.is_administrator():
            cod_id = request.args.get('id')
            grupo = Grupo.query.filter_by(cod_grupo = cod_id).one()
            db.session.delete(grupo)
            db.session.commit()
            return listar_usuarios()
        return redirect(url_for('main.index'))
    except:
        abort(500)

@admin.route('/atualizar_grupo', methods=['GET','POST'])
@login_required
def atualizar_grupo():
    """ Abre uma pagina com formulario para atualizar dados de um grupo especificado por id pela url """
    try:
        if current_user.is_administrator():
            cod_id = request.args.get('id')
            grupo = Grupo.query.filter_by(cod_grupo = cod_id).one()
            if request.method == 'POST':
                grupo.grupo_nome = request.form['grupo']
                db.session.commit()
                return listar_usuarios()
            return render_template('admin/atualizar_grupo.html', grupo=grupo)
        return redirect(url_for('main.index'))
    except:
        abort(500)

@admin.route('/resetar_dados')
@login_required
def resetar_dados():
    """ Resetar dados de todos os usuarios ou de um unico especificado por url """
    try:
        if current_user.is_administrator():
            if request.args.get('id') == None:
                usuarios = Usuario.query.all()
                for usuario in usuarios:
                    usuario.questoes_acertadas = 0
                    usuario.numero_jogos = 0
            if request.args.get('id') != None:
                cod_id = request.args.get('id')
                usuario = Usuario.query.filter_by(cod_usuario = cod_id).one()
                usuario.questoes_acertadas = 0
                usuario.numero_jogos = 0
            db.session.commit()
            return redirect(url_for('main.ranking'))
        return redirect(url_for('main.index'))
    except:
        abort(500)