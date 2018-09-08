""" usuarios informacoes e categoria

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
    op.add_column('usuario', sa.Column('senha_hash', sa.String(length=128)))
    op.add_column('usuario', sa.Column('questoes_acertadas', sa.Integer(), nullable=False))
    op.create_table('categoria',
    sa.Column('cod_categoria', sa.Integer(), nullable=False),
    sa.Column('categoria_nome', sa.String(length=32)),
    sa.Column('categoria_padrao', sa.Boolean, nullable=False),
    sa.PrimaryKeyConstraint('cod_categoria'),
    sa.UniqueConstraint('categoria_nome')
    )
    op.create_index('ix_categoria_categoria_padrao', 'categoria', ['categoria_padrao'], unique=True)

def downgrade():
    op.drop_index('ix_categoria_categoria_padrao', 'categoria')
    op.drop_column('usuario', 'senha_hash')
    op.drop_column('usuario', 'questoes_acertadas')
    op.drop_table('categoria')