""" initial migration

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
    op.create_table('grupo',
    sa.Column('cod_grupo', sa.Integer(), nullable=False),
    sa.Column('grupo_nome', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('cod_grupo'),
    sa.UniqueConstraint('grupo_nome')
    )
    op.create_table('usuario',
    sa.Column('cod_usuario', sa.Integer(), nullable=False),
    sa.Column('usuario', sa.String(length=64), nullable=True),
    sa.Column('cod_grupo', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cod_grupo'], ['grupo.cod_grupo'],),
    sa.PrimaryKeyConstraint('cod_usuario')
    )
    op.create_index('ix_usuario_usuario', 'usuario', ['usuario'], unique=True)


def downgrade():
    op.drop_index('ix_usuario_usuario', 'usuario')
    op.drop_table('usuario')
    op.drop_table('grupo')
