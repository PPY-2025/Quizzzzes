import pytest
import json
from backend.models import db, Question, Quiz
from backend.services import dbService
from app import create_app  # adjust to your actual app file name


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # in-memory DB for fast tests
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })

    with app.app_context():
        db.create_all()
        dbService.populate_dummy_data()  # populate with dummy quizzes and questions

    yield app

    # Teardown after tests
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_get_quizzes(client):
    resp = client.get('/quizzes')
    assert resp.status_code == 200
    quizzes = resp.get_json()
    assert isinstance(quizzes, list)
    assert len(quizzes) > 0
    assert "id" in quizzes[0] and "name" in quizzes[0]


def test_start_quiz_success(client):
    # assuming geography quiz id=1 (from dummy data)
    resp = client.get('/start', query_string={"quiz_id": 1})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["question_index"] == 0
    assert data["score"] == 0
    assert "question" in data
    assert "id" in data["question"]
    assert "text" in data["question"]
    assert "options" in data["question"]


def test_start_quiz_missing_quiz_id(client):
    resp = client.get('/start')
    assert resp.status_code == 400
    data = resp.get_json()
    assert "error" in data


def test_start_quiz_not_found(client):
    resp = client.get('/start', query_string={"quiz_id": 9999})
    assert resp.status_code == 404
    data = resp.get_json()
    assert "error" in data


def test_submit_answer_flow(client):
    # Start quiz to get first question
    start_resp = client.get('/start', query_string={"quiz_id": 1})
    start_data = start_resp.get_json()

    question = start_data["question"]
    question_index = start_data["question_index"]
    score = start_data["score"]
    quiz_id = start_data["quiz_id"]

    # Submit correct answer for first question
    resp = client.post('/submit_answer', json={
        "question_id": question["id"],
        "user_answer": "Paris",  # correct answer for first question in dummy data
        "question_index": question_index,
        "score": score,
        "quiz_id": quiz_id
    })

    assert resp.status_code == 200
    data = resp.get_json()
    assert ("question" in data or "finished" in data)
    assert "score" in data

    # If not finished, submit next question with wrong answer
    if not data.get("finished"):
        next_question = data["question"]
        next_index = data["question_index"]
        new_score = data["score"]

        resp2 = client.post('/submit_answer', json={
            "question_id": next_question["id"],
            "user_answer": "WrongAnswer",
            "question_index": next_index,
            "score": new_score,
            "quiz_id": quiz_id
        })
        assert resp2.status_code == 200
        data2 = resp2.get_json()
        assert "score" in data2
