format:
	ruff check --select I --fix ./
	ruff format src/

lint:
	ruff check src/

apply_migrate:
	alembic upgrade head

test:
	alembic upgrade head
	python3 -m pytest -v --disable-warnings --asyncio-mode=auto