#инструкция для запуска

```bash
python -m venv venv
```

```bash
.\venv\Scripts\activate
```

```bash
pip install -r requirements.txt
```

```bash
alembic upgrade head
```

```bash
docker-compose up -d
```

```bash
waitress-serve --port=9090 src.main:application
```