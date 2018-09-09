""" categoria table

Revision ID: 9a94275ae421
Revises: 375f0af244b6
Create Date: 2018-09-08 03:24:56.283902

"""

# revision identifiers, used by Alembic.
revision = '9a94275ae421'
down_revision = '375f0af244b6'

from alembic import op
import sqlalchemy as sa


def upgrade():
    """ Executa as seguintes tarefas no banco de dados """
    op.create_table(
        'categorias',
        sa.Column('cod_categoria', sa.Integer(), nullable=False),
        sa.Column('categoria_nome', sa.String(length=32)),
        sa.Column('categoria_padrao', sa.Boolean, nullable=False),
        sa.PrimaryKeyConstraint('cod_categoria'),
        sa.UniqueConstraint('categoria_nome')
    )

    op.create_index('ix_categorias_categoria_padrao', 'categorias', ['categoria_padrao'], unique=False)

def downgrade():
    """ Executa as seguintes tarefas no banco de dados """
    op.drop_index('ix_categorias_categoria_padrao', 'categorias')
    op.drop_table('categorias')
