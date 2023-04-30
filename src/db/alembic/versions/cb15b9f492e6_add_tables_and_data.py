"""Add tables and data

Revision ID: cb15b9f492e6
Revises: 
Create Date: 2023-02-25 07:07:46.483100

"""
import json
import os

from alembic import op
import sqlalchemy as sa
from sqlalchemy import table

# revision identifiers, used by Alembic.
revision = 'cb15b9f492e6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    countries = op.create_table('countries',
                                sa.Column('alpha_2_iso_code', sa.String(length=2), nullable=False),
                                sa.Column('name', sa.String(), nullable=False),
                                sa.Column('company_number_regex', sa.String(), nullable=False),
                                sa.Column('created_at', sa.DateTime(), nullable=False),
                                sa.Column('updated_at', sa.DateTime(), nullable=False),
                                sa.PrimaryKeyConstraint('alpha_2_iso_code'),
                                sa.UniqueConstraint('name')
                                )
    with open(os.path.join(os.path.dirname(__file__), "../sample_data/sample_countries.json")) as f:
        country_data = f.read()
    op.bulk_insert(countries, json.loads(country_data))
    op.create_table('companies',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('company_number', sa.String(length=100), nullable=False),
                    sa.Column('country_alpha_2_iso_code', sa.String(length=2), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['country_alpha_2_iso_code'], ['countries.alpha_2_iso_code'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_companies_id'), 'companies', ['id'], unique=False)
    op.create_table('scores',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('company_id', sa.Integer(), nullable=False),
                    sa.Column('year', sa.Integer(), nullable=False),
                    sa.Column('zscore', sa.Float(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_scores_id'), 'scores', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_scores_id'), table_name='scores')
    op.drop_table('scores')
    op.drop_index(op.f('ix_companies_id'), table_name='companies')
    op.drop_table('companies')
    op.drop_table('countries')
    # ### end Alembic commands ###