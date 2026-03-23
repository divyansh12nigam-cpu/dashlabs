"""Tests for webhook endpoints."""
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.config import settings

client = TestClient(app)


def test_health():
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_webhook_verify_success():
    resp = client.get("/webhook", params={
        "hub.mode": "subscribe",
        "hub.verify_token": settings.VERIFY_TOKEN,
        "hub.challenge": "test_challenge_123",
    })
    assert resp.status_code == 200
    assert resp.text == "test_challenge_123"


def test_webhook_verify_failure():
    resp = client.get("/webhook", params={
        "hub.mode": "subscribe",
        "hub.verify_token": "wrong_token",
        "hub.challenge": "test_challenge_123",
    })
    assert resp.status_code == 403


def test_webhook_post_empty():
    resp = client.post("/webhook", json={"entry": []})
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_webhook_post_status_update():
    """Status updates (no messages key) should return ok without processing."""
    resp = client.post("/webhook", json={
        "entry": [{
            "changes": [{
                "value": {
                    "statuses": [{"id": "123", "status": "delivered"}]
                }
            }]
        }]
    })
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
