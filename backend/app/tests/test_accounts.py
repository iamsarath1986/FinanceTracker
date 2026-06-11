ACCOUNT_PAYLOAD = {
    "name": "Test Savings",
    "type": "savings",
    "currency": "USD",
    "opening_balance": 1000.0,
}


def test_create_account(client, auth_headers):
    res = client.post("/accounts", json=ACCOUNT_PAYLOAD, headers=auth_headers)
    assert res.status_code == 201
    data = res.json()
    assert data["name"] == "Test Savings"
    assert data["current_balance"] == 1000.0


def test_list_accounts(client, auth_headers):
    client.post("/accounts", json=ACCOUNT_PAYLOAD, headers=auth_headers)
    res = client.get("/accounts", headers=auth_headers)
    assert res.status_code == 200
    assert len(res.json()) == 1


def test_get_account(client, auth_headers):
    created = client.post("/accounts", json=ACCOUNT_PAYLOAD, headers=auth_headers).json()
    res = client.get(f"/accounts/{created['id']}", headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["id"] == created["id"]


def test_get_account_not_found(client, auth_headers):
    res = client.get("/accounts/99999", headers=auth_headers)
    assert res.status_code == 404


def test_update_account(client, auth_headers):
    created = client.post("/accounts", json=ACCOUNT_PAYLOAD, headers=auth_headers).json()
    res = client.patch(
        f"/accounts/{created['id']}",
        json={"name": "Updated Name"},
        headers=auth_headers,
    )
    assert res.status_code == 200
    assert res.json()["name"] == "Updated Name"
    assert res.json()["currency"] == "USD"


def test_delete_account(client, auth_headers):
    created = client.post("/accounts", json=ACCOUNT_PAYLOAD, headers=auth_headers).json()
    res = client.delete(f"/accounts/{created['id']}", headers=auth_headers)
    assert res.status_code == 204
    res = client.get(f"/accounts/{created['id']}", headers=auth_headers)
    assert res.status_code == 404
