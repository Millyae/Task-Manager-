import pytest
from uuid import UUID
from task_manager.app.schemas import *


def test_create_task(test_client):
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "status": "created"
    }

    response = test_client.post("/tasks/", json=task_data)
    assert response.status_code == 200
    task = response.json()

    assert task["title"] == task_data["title"]
    assert task["description"] == task_data["description"]
    assert task["status"] == task_data["status"]
    assert UUID(task["uuid"])


def test_get_tasks(test_client):
    response = test_client.get("/tasks/")
    assert response.status_code == 200
    tasks = response.json()
    assert isinstance(tasks, list)
    assert len(tasks) > 0


def test_get_task(test_client):
    task_data = {"title": "Test Get Task", "description": "Test"}
    create_response = test_client.post("/tasks/", json=task_data)
    task_uuid = create_response.json()["uuid"]

    response = test_client.get(f"/tasks/{task_uuid}")
    assert response.status_code == 200
    task = response.json()
    assert task["uuid"] == task_uuid
    assert task["title"] == task_data["title"]


def test_update_task(test_client):
    task_data = {"title": "Original Title", "description": "Original"}
    create_response = test_client.post("/tasks/", json=task_data)
    task_uuid = create_response.json()["uuid"]

    update_data = {"title": "Updated Title", "status": "in_progress"}
    response = test_client.put(f"/tasks/{task_uuid}", json=update_data)
    assert response.status_code == 200
    task = response.json()

    assert task["title"] == update_data["title"]
    assert task["status"] == update_data["status"]
    assert task["description"] == task_data["description"]


def test_delete_task(test_client):
    task_data = {"title": "To Delete", "description": "Will be deleted"}
    create_response = test_client.post("/tasks/", json=task_data)
    task_uuid = create_response.json()["uuid"]

    response = test_client.delete(f"/tasks/{task_uuid}")
    assert response.status_code == 200

    get_response = test_client.get(f"/tasks/{task_uuid}")
    assert get_response.status_code == 404


def test_get_nonexistent_task(test_client):
    response = test_client.get("/tasks/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404