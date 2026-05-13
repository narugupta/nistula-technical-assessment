FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# running as a module keeps python package imports stable inside docker
CMD ["sh", "-c", "python -m app.scripts.wait_for_db && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]