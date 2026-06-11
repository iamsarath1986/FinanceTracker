def test_login_success(client):
    res = client.post("/auth/login", json={"password": "8mvNd5Iam@Fine2026#App9uRY"})
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    res = client.post("/auth/login", json={"password": "wrongpassword"})
    assert res.status_code == 401


def test_protected_route_without_token(client):
    res = client.get("/accounts")
    assert res.status_code == 401


def test_protected_route_with_invalid_token(client):
    res = client.get("/accounts", headers={"Authorization": "Bearer invalid.token.here"})
    assert res.status_code == 401
