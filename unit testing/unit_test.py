from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

#======/api/query TEST======
def test_query_success():
    cookies = {"uj_student_id": "2312345", "uj_major": "cs"}

    client.cookies.update(cookies)

    payload = {"question": "ما هو الذكاء الاصطناعي؟"}
    response = client.post("/api/query", json=payload)
    assert response.status_code == 200
    assert "answer" in response.json()

#Missing cookies
def test_query_missing_cookies():
    client.cookies.clear()
    payload = {"question": "هل يوجد نادي؟"}
    response = client.post("/api/query", json=payload)
    assert response.status_code == 400
    assert "Student ID and major are required" in response.text

#StudentID shorter than 7 Numbers
def test_query_invalid_student_id():
    cookies = {"uj_student_id": "12345", "uj_major": "cs"}
    client.cookies.update(cookies)

    payload = {"question": "ما هو الأمن السيبراني؟"}
    response = client.post("/api/query", json=payload)
    assert response.status_code == 400
    assert "Student ID must be 7 digits" in response.text

# Invalid major key
def test_query_invalid_major():
    cookies = {"uj_student_id": "2312345", "uj_major": "xyz"}
    client.cookies.update(cookies)

    payload = {"question": "هل يوجد تخصص جديد؟"}
    response = client.post("/api/query", json=payload)
    assert response.status_code == 400
    assert "Invalid major value" in response.text

# Question short
def test_query_too_short_question():
    cookies = {"uj_student_id": "2312345", "uj_major": "cs"}
    client.cookies.update(cookies)

    payload = {"question": "ها"}  # less than 3 characters
    response = client.post("/api/query", json=payload)
    assert response.status_code == 400
    assert "Question is too short" in response.text

#======/api/feedback TEST======
valid_cookies = {"uj_student_id": "2312345", "uj_major": "cs"}
valid_payload = {
    "question": "ما هو الذكاء الاصطناعي؟",
    "answer": "هو فرع من علوم الحاسب",
    "feedback": "good",
    "question_id": "q123",
    "response_time": 1.2
}

#Missing cookies
def test_feedback_missing_cookies():
    client.cookies.clear()

    response = client.post("/api/feedback", json=valid_payload)
    assert response.status_code == 400
    assert "Student ID and major are required" in response.text

#Invalid studentID less than 7 Numbers
def test_feedback_invalid_student_id():
    cookies = {"uj_student_id": "1234", "uj_major": "cs"}
    client.cookies.update(cookies)

    response = client.post("/api/feedback", json=valid_payload)
    assert response.status_code == 400
    assert "Student ID must be 7 digits" in response.text

#Invalid major key
def test_feedback_invalid_major():
    cookies = {"uj_student_id": "2312345", "uj_major": "xyz"}
    client.cookies.update(cookies)
    response = client.post("/api/feedback", json=valid_payload)
    assert response.status_code == 400
    assert "Invalid major value" in response.text

#Empty field value
def test_feedback_empty_field():
    bad_payload = valid_payload.copy()
    bad_payload["answer"] = ""  #empty field

    client.cookies.update(valid_cookies)

    response = client.post("/api/feedback", json=bad_payload)
    assert response.status_code == 400
    assert "cannot be empty" in response.text

#Invalid feedback value
def test_feedback_invalid_feedback_value():
    bad_payload = valid_payload.copy()
    bad_payload["feedback"] = "average"
    client.cookies.update(valid_cookies)

    response = client.post("/api/feedback", json=bad_payload)
    assert response.status_code == 400
    assert "Feedback must be 'good' or 'bad'" in response.text

#Invalid response_time not float
def test_feedback_response_time_not_float():
    bad_payload = valid_payload.copy()
    bad_payload["response_time"] = "fast"
    client.cookies.update(valid_cookies)

    response = client.post("/api/feedback", json=bad_payload)
    assert response.status_code == 422

#Invalid response_time negative number
def test_feedback_response_time_negative():
    bad_payload = valid_payload.copy()
    bad_payload["response_time"] = -5.0

    client.cookies.update(valid_cookies)

    response = client.post("/api/feedback", json=bad_payload)
    assert response.status_code == 400
    assert "Response time must be a positive float" in response.text

#Valid feedback submission
def test_feedback_success():
    client.cookies.update(valid_cookies)

    response = client.post("/api/feedback", json=valid_payload)
    assert response.status_code == 200
    assert "Feedback saved successfully" in response.text

