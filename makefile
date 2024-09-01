# Variables
ALEMBIC_DIR=alembic
MIGRATION_DIR=$(ALEMBIC_DIR)/versions
DATABASE_URL=sqlite:///./test.db

# Commands
migrations:
	@echo "Generating migration script..."
	@if [ -z "$(msg)" ]; then \
		msg="Auto-generated migration"; \
	fi; \
	alembic revision --autogenerate -m "$msg"

migrate:
	@echo "Applying migrations..."
	alembic upgrade head
