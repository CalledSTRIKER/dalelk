import pytest
from fastapi.testclient import TestClient
from main import app, banned_ips, violations

client = TestClient(app)

# reset the rate limit
@pytest.fixture(autouse=True)
def reset_rate_limit():
    banned_ips.clear()
    violations.clear()
    app.state.limiter._storage.reset()
    yield
    banned_ips.clear()
    violations.clear()


COOKIES = {"uj_student_id": "2312345", "uj_major": "cs"}
PAYLOAD = {"question": "ما هو الذكاء الاصطناعي؟"}


def send_requests(count):
    """Send N requests and return list of status codes"""
    results = []
    for _ in range(count):
        client.cookies.update(COOKIES)
        r = client.post("/api/query", json=PAYLOAD)
        results.append(r.status_code)
    return results


# (429 test) send 4 كلها تنجح, then 5 fails
def test_rate_limit_429():
    # First 4 should be 200
    results = send_requests(4)
    assert all(s == 200 for s in results), f"Expected all 200, got: {results}"

    # 5th should be 429
    client.cookies.update(COOKIES)
    r = client.post("/api/query", json=PAYLOAD)
    assert r.status_code == 429
    assert "Too many requests" in r.text
    print("\n 429 Too Many Requests triggered correctly after 4 requests")


# ban test  violation 3 times then 403 banned
def test_rate_limit_ban():

    def trigger_violation():
        
        send_requests(4)


    trigger_violation()  # violation count = 1 429
    trigger_violation()  # violation count = 2 429


    # next request should be 403 banned
    client.cookies.update(COOKIES)
    r = client.post("/api/query", json=PAYLOAD)
    assert r.status_code == 403
    assert "banned" in r.text
    print("\n 403 Ban triggered correctly after 3 violations")