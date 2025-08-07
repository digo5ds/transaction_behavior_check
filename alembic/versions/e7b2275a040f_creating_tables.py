"""Creating tables

Revision ID: e7b2275a040f
Revises:
Create Date: 2025-08-07 18:17:02.499473

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e7b2275a040f"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # pylint: disable=no-member
    op.create_table(
        "customer",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("age", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "account",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("account", sa.Integer(), nullable=True),
        sa.Column("agency", sa.Integer(), nullable=True),
        sa.Column("customer_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["customer_id"],
            ["customer.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "transaction",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("transaction_date", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("amount", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column(
            "channel",
            sa.Enum(
                "ATM",
                "TELLER",
                "INTERNET_BANKING",
                "MOBILE_BANKING",
                name="channelenum",
            ),
            nullable=False,
        ),
        sa.Column("suspect", sa.Boolean(), nullable=True),
        sa.Column(
            "type", sa.Enum("CREDIT", "DEBIT", name="transactiontype"), nullable=False
        ),
        sa.Column("origin_account_id", sa.Integer(), nullable=False),
        sa.Column("destination_account_id", sa.Integer(), nullable=False),
        sa.CheckConstraint("amount > 0", name="check_amount_positive"),
        sa.ForeignKeyConstraint(
            ["destination_account_id"],
            ["account.id"],
        ),
        sa.ForeignKeyConstraint(
            ["origin_account_id"],
            ["account.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""

    # pylint: disable=no-member
    op.drop_table("transaction")
    op.drop_table("account")
    op.drop_table("customer")
    # ### end Alembic commands ###
