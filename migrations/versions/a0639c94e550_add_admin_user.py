""" add admin user

Revision ID: a0639c94e550
Revises: a0d13b7fb981
Create Date: 2018-09-09 18:26:12.158660

"""

# revision identifiers, used by Alembic.
revision = 'a0639c94e550'
down_revision = 'a0d13b7fb981'

from alembic import op
import sqlalchemy as sa
from app import db
from app.models import Usuario


def upgrade():
    """ Executa as seguintes tarefas no banco de dados """
    admin = Usuario(email='admin@questionup.top',
                      usuario='admin',
                      senha='admin',
                      cod_grupo=1)
    usuario = Usuario(email='usuario@questionup.top',
                      usuario='usuario',
                      senha='usuario',
                      cod_grupo=0)
    db.session.add(admin)
    db.session.add(usuario)
    db.session.commit()

def downgrade():
    """ Executa as seguintes tarefas no banco de dados """
    admin = Usuario.query.filter_by(usuario='admin').first()
    usuario = Usuario.query.filter_by(usuario='usuario').first()
    db.session.remove(admin)
    db.session.remove(usuario)
    db.session.commit()
