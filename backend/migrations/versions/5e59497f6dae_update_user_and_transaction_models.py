"""Update user and transaction models

Revision ID: 5e59497f6dae
Revises: 
Create Date: 2024-03-25 19:45:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime, timedelta
import random
from werkzeug.security import generate_password_hash

# revision identifiers, used by Alembic.
revision = '5e59497f6dae'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create tables
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('hashed_password', sa.String(length=512), nullable=False),
        sa.Column('full_name', sa.String(length=100), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    op.create_table(
        'bank_accounts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('account_name', sa.String(length=100), nullable=False),
        sa.Column('account_type', sa.String(length=50), nullable=False),
        sa.Column('balance', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'transactions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('bank_account_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.Column('description', sa.String(length=200), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('merchant', sa.String(length=100), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['bank_account_id'], ['bank_accounts.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Insert sample data
    # Create a sample user with password 'demo123'
    connection = op.get_bind()
    hashed_password = generate_password_hash('demo123')
    connection.execute(sa.text(f"""
        INSERT INTO users (email, hashed_password, full_name, created_at)
        VALUES ('demo@example.com', '{hashed_password}', 'Demo User', NOW())
        RETURNING id
    """))
    result = connection.execute(sa.text("SELECT id FROM users WHERE email = 'demo@example.com'"))
    user_id = result.fetchone()[0]

    # Create sample bank accounts
    connection.execute(sa.text(f"""
        INSERT INTO bank_accounts (user_id, account_name, account_type, balance, created_at)
        VALUES 
        ({user_id}, 'Main Checking', 'checking', 5000.00, NOW()),
        ({user_id}, 'Savings', 'savings', 10000.00, NOW())
    """))

    # Get the bank account IDs
    result = connection.execute(sa.text("SELECT id FROM bank_accounts WHERE user_id = " + str(user_id)))
    account_ids = [row[0] for row in result.fetchall()]

    # Generate sample transactions for the past year
    categories = ['Food & Dining', 'Transportation', 'Shopping', 'Bills & Utilities', 'Entertainment', 'Healthcare', 'Travel', 'Education']
    merchants = ['Walmart', 'Target', 'Amazon', 'Netflix', 'Spotify', 'Uber', 'Restaurant', 'Grocery Store', 'Gas Station', 'Pharmacy']
    
    # Generate transactions for each month of the past year
    for month_offset in range(12):
        # Calculate the date range for this month
        date = datetime.now() - timedelta(days=30 * month_offset)
        start_date = date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)

        # Generate 10-20 transactions per month
        num_transactions = random.randint(10, 20)
        for _ in range(num_transactions):
            transaction_date = start_date + timedelta(
                days=random.randint(0, (end_date - start_date).days),
                hours=random.randint(0, 23)
            )
            amount = round(random.uniform(10, 500), 2)
            category = random.choice(categories)
            merchant = random.choice(merchants)
            account_id = random.choice(account_ids)

            connection.execute(sa.text(f"""
                INSERT INTO transactions (bank_account_id, date, description, amount, category, merchant, created_at)
                VALUES (
                    {account_id},
                    '{transaction_date}',
                    '{merchant} - {category}',
                    {amount},
                    '{category}',
                    '{merchant}',
                    NOW()
                )
            """))

def downgrade():
    op.drop_table('transactions')
    op.drop_table('bank_accounts')
    op.drop_table('users') 