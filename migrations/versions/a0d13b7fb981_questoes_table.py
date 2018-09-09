""" questao table

Revision ID: a0d13b7fb981
Revises: 9a94275ae421
Create Date: 2018-09-08 03:36:54.722472

"""

# revision identifiers, used by Alembic.
revision = 'a0d13b7fb981'
down_revision = '9a94275ae421'

from alembic import op
import sqlalchemy as sa


def upgrade():
    """ Executa as seguintes tarefas no banco de dados """
    op.create_table(
        'questoes',
        sa.Column('cod_questao', sa.Integer(), nullable=False),
        sa.Column('cod_categoria', sa.Integer(), nullable=True),
        sa.Column('cod_usuario', sa.Integer(), nullable=True),
        sa.Column('questao', sa.String(length=512), nullable=False),
        sa.Column('alternativa1', sa.String(length=256), nullable=False),
        sa.Column('alternativa2', sa.String(length=256), nullable=False),
        sa.Column('alternativa3', sa.String(length=256), nullable=False),
        sa.Column('alternativa4', sa.String(length=256), nullable=False),
        sa.Column('alternativa5', sa.String(length=256), nullable=False),
        sa.Column('alternativa_correta', sa.String(length=15), nullable=False),
        sa.ForeignKeyConstraint(['cod_categoria'], ['categorias.cod_categoria'],),
        sa.ForeignKeyConstraint(['cod_usuario'], ['usuarios.cod_usuario'],),
        sa.PrimaryKeyConstraint('cod_questao')
    )

def downgrade():
    """ Executa as seguintes tarefas no banco de dados """
    op.drop_table('questoes')
