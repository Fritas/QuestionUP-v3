""" informacoes do usuario

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
    op.add_column('usuario', sa.Column('membro_desde', sa.DateTime(), nullable=True))
    op.add_column('usuario', sa.Column('email', sa.String(length=64), unique=True))
    op.create_index('ix_usuario_email', 'usuario', ['email'], unique=True)

def downgrade():
    op.drop_index('ix_usuario_email', 'usuario')
    op.drop_column('usuario', 'email')
    op.drop_column('usuario', 'membro_desde')
