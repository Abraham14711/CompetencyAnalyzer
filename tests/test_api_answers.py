import pytest
import requests
from competencyAnalyser.api.models import *

from fastapi.testclient import TestClient
from competencyAnalyser.scripts.competencyAnalyser import app

client = TestClient(app)


FAKE_TIME = "2024-07-07T12:16:15.847Z"


@pytest.fixture
def date():
    return FAKE_TIME


@pytest.fixture
def uuid():
    return "6b2fac26-c9d9-475f-8906-7366c6dcae89"


@pytest.fixture
def answer(uuid, date):
    return {
        "user_id": uuid,
        "content": "test",
        "created_at": date,
        "updated_at": date
    }


@pytest.fixture
def updated_answer(uuid, date):
    return {
        "content": "updated test data",
        "updated_at": date
    }


@pytest.fixture
def question(uuid):
    return {
        "id": uuid,
        "content": "test",
        "competency_id": uuid
    }


@pytest.fixture
def updated_question(uuid):
    return {
        "content": "updated test data",
        "competency_id": uuid
    }


@pytest.fixture
def competency(uuid):
    return {
        "id": uuid,
        "title": "test"
    }


@pytest.fixture
def updated_competency():
    return {
        "title": "updated test"
    }


def test_create_competency(competency):
    post_response = client.post(
        "http://127.0.0.1:8000/api/competencies",
        json=competency
    )
    assert post_response.status_code == requests.status_codes.codes.created


def test_get_all_competencies():
    get_response = client.get('http://127.0.0.1:8000/api/competencies')
    assert get_response.status_code == requests.status_codes.codes.ok


def test_get_competency(uuid):
    get_response = client.get(
        f"http://127.0.0.1:8000/api/competencies/{uuid}"
    )
    assert get_response.status_code == requests.status_codes.codes.ok


def test_update_competency(uuid, updated_competency):
    put_response = client.put(
        f"http://127.0.0.1:8000/api/competencies/{uuid}",
        json=updated_competency
    )
    assert put_response.status_code == requests.status_codes.codes.ok


def test_create_question(question):
    post_response = client.post(
        "http://127.0.0.1:8000/api/questions",
        json=question
    )
    assert post_response.status_code == requests.status_codes.codes.created


def test_get_all_questions():
    get_response = client.get('http://127.0.0.1:8000/api/questions')
    assert get_response.status_code == requests.status_codes.codes.ok


def test_get_question(uuid):
    get_response = client.get(
        f"http://127.0.0.1:8000/api/questions/{uuid}"
    )
    assert get_response.status_code == requests.status_codes.codes.ok


def test_update_question(uuid, updated_question):
    put_response = client.put(
        f"http://127.0.0.1:8000/api/questions/{uuid}",
        json=updated_question
    )
    assert put_response.status_code == requests.status_codes.codes.ok


def test_create_answer(answer):
    post_response = client.post(
        "http://127.0.0.1:8000/api/answers",
        json=answer
    )
    assert post_response.status_code == requests.status_codes.codes.created


def test_get_all_answers():
    get_response = client.get('http://127.0.0.1:8000/api/answers')
    assert get_response.status_code == requests.status_codes.codes.ok


def test_get_answer(uuid):
    get_response = client.get(
        f"http://127.0.0.1:8000/api/answers/{uuid}"
    )
    assert get_response.status_code == requests.status_codes.codes.ok


def test_update_answer(uuid, updated_answer):
    put_response = client.put(
        f"http://127.0.0.1:8000/api/answers/{uuid}",
        json=updated_answer
    )
    assert put_response.status_code == requests.status_codes.codes.ok


def test_delete_answer(uuid):
    delete_response = client.delete(
        f"http://127.0.0.1:8000/api/answers/{uuid}"
    )
    assert delete_response.status_code == requests.status_codes.codes.ok


def test_delete_question(uuid):
    delete_response = client.delete(
        f"http://127.0.0.1:8000/api/questions/{uuid}"
    )
    assert delete_response.status_code == requests.status_codes.codes.ok


def test_delete_competency(uuid):
    delete_response = client.delete(
        f"http://127.0.0.1:8000/api/competencies/{uuid}"
    )
    assert delete_response.status_code == requests.status_codes.codes.ok
