""" add grupos

Revision ID: 1a189273fc8e
Revises: a0639c94e550
Create Date: 2018-09-09 19:01:30.068832

"""

# revision identifiers, used by Alembic.
revision = '1a189273fc8e'
down_revision = 'a0639c94e550'

from alembic import op
import sqlalchemy as sa
from app import db
from app.models import Grupo

def upgrade():
    """ Executa as seguintes tarefas no banco de dados """
    grupo_usuario = Grupo(grupo_nome='Usuário', cod_grupo=0)
    grupo_admin = Grupo(grupo_nome='Administrador', cod_grupo=1)
    db.session.add(grupo_usuario)
    db.session.add(grupo_admin)
    db.session.commit()

def downgrade():
    """ Executa as seguintes tarefas no banco de dados """
    todos_grupo = Grupo.query.all()
    db.session.remove(todos_grupo)
    db.session.commit()