""" grupo table

Revision ID: 2f9a3ba45b00
Revises: None
Create Date: 2018-09-08 03:01:37.405213

"""

# revision identifiers, used by Alembic.
revision = '2f9a3ba45b00'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    """ Executa as seguintes tarefas no banco de dados """
    op.create_table(
        'grupos',
        sa.Column('cod_grupo', sa.Integer(), nullable=False),
        sa.Column('grupo_nome', sa.String(length=64), nullable=True),
        sa.PrimaryKeyConstraint('cod_grupo'),
        sa.UniqueConstraint('grupo_nome')
    )

def downgrade():
    """ Executa as seguintes tarefas no banco de dados """
    op.drop_table('grupos')
