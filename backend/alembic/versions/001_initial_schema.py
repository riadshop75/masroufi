"""Initial schema creation

Revision ID: 001
Revises:
Create Date: 2025-04-23

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create enum types
    frequency_enum = postgresql.ENUM('weekly', 'monthly', 'yearly', name='frequencyenum', create_type=True)
    frequency_enum.create(op.get_bind(), checkfirst=True)

    # users table
    op.create_table(
        'users',
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('user_id'),
        sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # categories table
    op.create_table(
        'categories',
        sa.Column('category_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('emoji', sa.String(length=10), nullable=True),
        sa.Column('color', sa.String(length=7), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
        sa.PrimaryKeyConstraint('category_id')
    )
    op.create_index(op.f('ix_categories_user_id'), 'categories', ['user_id'], unique=False)

    # expenses table
    op.create_table(
        'expenses',
        sa.Column('expense_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('category_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('note', sa.Text(), nullable=True),
        sa.Column('is_recurring', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['category_id'], ['categories.category_id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
        sa.PrimaryKeyConstraint('expense_id')
    )
    op.create_index(op.f('ix_expenses_category_id'), 'expenses', ['category_id'], unique=False)
    op.create_index(op.f('ix_expenses_date'), 'expenses', ['date'], unique=False)
    op.create_index(op.f('ix_expenses_user_id'), 'expenses', ['user_id'], unique=False)

    # recurring_expenses table
    op.create_table(
        'recurring_expenses',
        sa.Column('recurring_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('expense_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('frequency', frequency_enum, nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('last_execution_date', sa.Date(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['expense_id'], ['expenses.expense_id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
        sa.PrimaryKeyConstraint('recurring_id'),
        sa.UniqueConstraint('expense_id')
    )
    op.create_index(op.f('ix_recurring_expenses_user_id'), 'recurring_expenses', ['user_id'], unique=False)

    # budgets table
    op.create_table(
        'budgets',
        sa.Column('budget_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('category_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('monthly_limit', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('alert_threshold', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['category_id'], ['categories.category_id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
        sa.PrimaryKeyConstraint('budget_id')
    )
    op.create_index(op.f('ix_budgets_category_id'), 'budgets', ['category_id'], unique=False)
    op.create_index(op.f('ix_budgets_user_id'), 'budgets', ['user_id'], unique=False)

    # api_tokens table
    op.create_table(
        'api_tokens',
        sa.Column('token_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('token_hash', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('scopes', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('last_used', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
        sa.PrimaryKeyConstraint('token_id'),
        sa.UniqueConstraint('token_hash')
    )
    op.create_index(op.f('ix_api_tokens_token_hash'), 'api_tokens', ['token_hash'], unique=True)
    op.create_index(op.f('ix_api_tokens_user_id'), 'api_tokens', ['user_id'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_api_tokens_user_id'), table_name='api_tokens')
    op.drop_index(op.f('ix_api_tokens_token_hash'), table_name='api_tokens')
    op.drop_table('api_tokens')

    op.drop_index(op.f('ix_budgets_user_id'), table_name='budgets')
    op.drop_index(op.f('ix_budgets_category_id'), table_name='budgets')
    op.drop_table('budgets')

    op.drop_index(op.f('ix_recurring_expenses_user_id'), table_name='recurring_expenses')
    op.drop_table('recurring_expenses')

    op.drop_index(op.f('ix_expenses_user_id'), table_name='expenses')
    op.drop_index(op.f('ix_expenses_date'), table_name='expenses')
    op.drop_index(op.f('ix_expenses_category_id'), table_name='expenses')
    op.drop_table('expenses')

    op.drop_index(op.f('ix_categories_user_id'), table_name='categories')
    op.drop_table('categories')

    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')

    frequency_enum = postgresql.ENUM('weekly', 'monthly', 'yearly', name='frequencyenum', create_type=True)
    frequency_enum.drop(op.get_bind(), checkfirst=True)
