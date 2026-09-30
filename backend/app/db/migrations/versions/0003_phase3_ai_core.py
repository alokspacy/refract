"""Phase 3 AI core tables

Revision ID: 0003_phase3_ai_core
Revises: 0002_phase2_extraction
Create Date: 2026-08-30 02:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '0003_phase3_ai_core'
down_revision: Union[str, None] = '0002_phase2_extraction'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Content Analyses
    op.create_table(
        'content_analyses',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('document_id', sa.String(length=36), sa.ForeignKey('documents.id', ondelete='CASCADE'), nullable=False),
        sa.Column('language', sa.String(length=10), nullable=False, server_default='en'),
        sa.Column('subject', sa.String(length=100), nullable=True),
        sa.Column('grade_hint', sa.String(length=50), nullable=True),
        sa.Column('complexity', sa.String(length=50), nullable=False, server_default='intermediate'),
        sa.Column('learning_objectives', sa.JSON(), nullable=False),
        sa.Column('concepts', sa.JSON(), nullable=False),
        sa.Column('vocabulary', sa.JSON(), nullable=False),
        sa.Column('extra_metadata', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_content_analyses_document_id'), 'content_analyses', ['document_id'], unique=True)

    # 2. Generated Variants
    op.create_table(
        'generated_variants',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('document_id', sa.String(length=36), sa.ForeignKey('documents.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('status', sa.String(length=30), nullable=False, server_default='PENDING'),
        sa.Column('profile_ids', sa.JSON(), nullable=False),
        sa.Column('profile_versions', sa.JSON(), nullable=False),
        sa.Column('metadata_overrides', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_generated_variants_document_id'), 'generated_variants', ['document_id'], unique=False)

    # 3. Generated Blocks
    op.create_table(
        'generated_blocks',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('variant_id', sa.String(length=36), sa.ForeignKey('generated_variants.id', ondelete='CASCADE'), nullable=False),
        sa.Column('source_block_id', sa.String(length=64), nullable=False),
        sa.Column('profile_id', sa.String(length=50), nullable=False),
        sa.Column('content', sa.JSON(), nullable=False),
        sa.Column('status', sa.String(length=30), nullable=False, server_default='PENDING'),
        sa.Column('prompt_version', sa.String(length=50), nullable=False, server_default='1.0.0'),
        sa.Column('model', sa.String(length=100), nullable=False),
        sa.Column('provider', sa.String(length=50), nullable=False),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_generated_blocks_variant_id'), 'generated_blocks', ['variant_id'], unique=False)
    op.create_index(op.f('ix_generated_blocks_source_block_id'), 'generated_blocks', ['source_block_id'], unique=False)
    op.create_index(op.f('ix_generated_blocks_profile_id'), 'generated_blocks', ['profile_id'], unique=False)

    # 4. Validation Results
    op.create_table(
        'validation_results',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('variant_id', sa.String(length=36), sa.ForeignKey('generated_variants.id', ondelete='CASCADE'), nullable=False),
        sa.Column('block_id', sa.String(length=36), sa.ForeignKey('generated_blocks.id', ondelete='CASCADE'), nullable=True),
        sa.Column('is_valid', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('grounded', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('unsupported_claims', sa.JSON(), nullable=False),
        sa.Column('warnings', sa.JSON(), nullable=False),
        sa.Column('errors', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_validation_results_variant_id'), 'validation_results', ['variant_id'], unique=False)
    op.create_index(op.f('ix_validation_results_block_id'), 'validation_results', ['block_id'], unique=False)

    # 5. Transformation Cache
    op.create_table(
        'transformation_cache',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('cache_key', sa.String(length=64), nullable=False),
        sa.Column('source_hash', sa.String(length=64), nullable=False),
        sa.Column('profile_id', sa.String(length=50), nullable=False),
        sa.Column('profile_version', sa.String(length=50), nullable=False),
        sa.Column('prompt_version', sa.String(length=50), nullable=False),
        sa.Column('model', sa.String(length=100), nullable=False),
        sa.Column('content', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_transformation_cache_cache_key'), 'transformation_cache', ['cache_key'], unique=True)
    op.create_index(op.f('ix_transformation_cache_source_hash'), 'transformation_cache', ['source_hash'], unique=False)

    # 6. Provider Usages
    op.create_table(
        'provider_usages',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('provider', sa.String(length=50), nullable=False),
        sa.Column('model', sa.String(length=100), nullable=False),
        sa.Column('operation', sa.String(length=100), nullable=False),
        sa.Column('prompt_tokens', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('completion_tokens', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('total_tokens', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('estimated_cost_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('provider_usages')
    op.drop_index(op.f('ix_transformation_cache_source_hash'), table_name='transformation_cache')
    op.drop_index(op.f('ix_transformation_cache_cache_key'), table_name='transformation_cache')
    op.drop_table('transformation_cache')
    op.drop_index(op.f('ix_validation_results_block_id'), table_name='validation_results')
    op.drop_index(op.f('ix_validation_results_variant_id'), table_name='validation_results')
    op.drop_table('validation_results')
    op.drop_index(op.f('ix_generated_blocks_profile_id'), table_name='generated_blocks')
    op.drop_index(op.f('ix_generated_blocks_source_block_id'), table_name='generated_blocks')
    op.drop_index(op.f('ix_generated_blocks_variant_id'), table_name='generated_blocks')
    op.drop_table('generated_blocks')
    op.drop_index(op.f('ix_generated_variants_document_id'), table_name='generated_variants')
    op.drop_table('generated_variants')
    op.drop_index(op.f('ix_content_analyses_document_id'), table_name='content_analyses')
    op.drop_table('content_analyses')
