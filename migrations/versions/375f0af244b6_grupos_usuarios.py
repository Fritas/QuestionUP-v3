""" grupos de usuarios

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
    op.add_column('grupo', sa.Column('grupo_padrao', sa.Boolean(), nullable=True))
    op.add_column('grupo', sa.Column('permisssoes', sa.Integer(), nullable=True))
    op.create_index('ix_grupo_grupo_padrao', 'grupo', ['grupo_padrao'], unique=True)

def downgrade():
    op.drop_index('ix_grupo_grupo_padrao', 'grupo')
    op.drop_column('grupo', 'permissoes')
    op.drop_column('grupo', 'grupo_padrao')
