"""Phase 2 extraction fields for documents table

Revision ID: 0002_phase2_extraction
Revises: 0001_initial_schema
Create Date: 2026-08-30 01:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '0002_phase2_extraction'
down_revision: Union[str, None] = '0001_initial_schema'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('documents', sa.Column('extraction_status', sa.String(length=50), nullable=False, server_default='PENDING'))
    op.add_column('documents', sa.Column('normalized_content', sa.JSON(), nullable=True))
    op.add_column('documents', sa.Column('extraction_warnings', sa.JSON(), nullable=True))
    op.add_column('documents', sa.Column('extracted_at', sa.DateTime(timezone=True), nullable=True))
    op.create_index(op.f('ix_documents_extraction_status'), 'documents', ['extraction_status'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_documents_extraction_status'), table_name='documents')
    op.drop_column('documents', 'extracted_at')
    op.drop_column('documents', 'extraction_warnings')
    op.drop_column('documents', 'normalized_content')
    op.drop_column('documents', 'extraction_status')
