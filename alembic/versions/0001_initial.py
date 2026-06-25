"""initial schema

Revision ID: 0001_initial
Revises: 
Create Date: 2026-06-25
"""

from alembic import op
import sqlalchemy as sa


revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)

    op.create_table(
        "repositories",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("url", sa.String(length=2048), nullable=False),
        sa.Column("owner", sa.String(length=255), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=True),
        sa.Column("default_branch", sa.String(length=255), nullable=True),
        sa.Column("commit_hash", sa.String(length=128), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("file_count", sa.Integer(), nullable=False),
        sa.Column("language_stats", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
    )
    op.create_index(op.f("ix_repositories_commit_hash"), "repositories", ["commit_hash"], unique=False)
    op.create_index(op.f("ix_repositories_status"), "repositories", ["status"], unique=False)
    op.create_index(op.f("ix_repositories_url"), "repositories", ["url"], unique=False)

    op.create_table(
        "ingestion_jobs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("repository_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("progress_pct", sa.Integer(), nullable=False),
        sa.Column("stage", sa.String(length=128), nullable=True),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("task_id", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"]),
    )
    op.create_index(op.f("ix_ingestion_jobs_repository_id"), "ingestion_jobs", ["repository_id"], unique=False)
    op.create_index(op.f("ix_ingestion_jobs_status"), "ingestion_jobs", ["status"], unique=False)

    op.create_table(
        "file_records",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("repository_id", sa.Integer(), nullable=False),
        sa.Column("path", sa.String(length=1024), nullable=False),
        sa.Column("language", sa.String(length=64), nullable=True),
        sa.Column("size", sa.Integer(), nullable=False),
        sa.Column("hash", sa.String(length=128), nullable=False),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"]),
    )
    op.create_index(op.f("ix_file_records_repository_id"), "file_records", ["repository_id"], unique=False)
    op.create_index(op.f("ix_file_records_hash"), "file_records", ["hash"], unique=False)
    op.create_index(op.f("ix_file_records_path"), "file_records", ["path"], unique=False)


def downgrade() -> None:
    op.drop_table("file_records")
    op.drop_table("ingestion_jobs")
    op.drop_table("repositories")
    op.drop_table("users")