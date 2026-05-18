# alembic/versions/xxxx_add_seed_data.py
from uuid import uuid4

from alembic import op
from sqlalchemy import table, column
from sqlalchemy import Integer, String, Boolean
import sqlalchemy as sa

# revision identifiers
revision = 'xxxx_add_seed_data'
down_revision = 'a5be8a23454b'
branch_labels = None
depends_on = None

role_table = table('roles',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('level', sa.Text(), nullable=True),
)

id1 = uuid4()
id2 = uuid4()

def upgrade():
    """Добавляем начальные данные"""
    
    # 1. Добавляем роли
    op.bulk_insert(role_table, [
        {'id': id1, 'name': 'admin', 'level': 1},
        {'id': id2, 'name': 'user', 'level': 5},
    ])
    

def downgrade():
    """Откатываем добавление данных"""
    op.execute(f"DELETE FROM roles WHERE id IN ({id1}, {id2})")
    