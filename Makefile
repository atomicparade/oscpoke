lint:
	ruff format oscpoke.py && ruff check oscpoke.py && mypy oscpoke.py
