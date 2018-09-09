""" usuario table

Revision ID: 375f0af244b6
Revises: 2f9a3ba45b00
Create Date: 2018-09-08 03:19:22.000647

"""

# revision identifiers, used by Alembic.
revision = '375f0af244b6'
down_revision = '2f9a3ba45b00'

from alembic import op
import sqlalchemy as sa


def upgrade():
    """ Executa as seguintes tarefas no banco de dados """
    op.create_table(
        'usuarios',
        sa.Column('cod_usuario', sa.Integer(), nullable=False),
        sa.Column('cod_grupo', sa.Integer(), nullable=True),
        sa.Column('usuario', sa.String(length=64), nullable=True),
        sa.Column('email', sa.String(length=64), unique=True),
        sa.Column('senha_hash', sa.String(length=128), nullable=False),
        sa.Column('questoes_acertadas', sa.Integer(), nullable=False),
        sa.Column('membro_desde', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['cod_grupo'], ['grupos.cod_grupo'],),
        sa.PrimaryKeyConstraint('cod_usuario')
    )

    op.create_index('ix_usuarios_usuario', 'usuarios', ['usuario'], unique=True)
    op.create_index('ix_usuarios_email', 'usuarios', ['email'], unique=True)


def downgrade():
    """ Executa as seguintes tarefas no banco de dados """
    op.drop_index('ix_usuarios_usuario', 'usuarios')
    op.drop_index('ix_usuarios_email', 'usuarios')
    op.drop_table('usuarios')
