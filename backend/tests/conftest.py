from fastapi.testclient import TestClient

from app.main import app


# keeping one shared client speeds tests up a lot
client = TestClient(app)