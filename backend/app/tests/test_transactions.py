from datetime import date


def _create_account(client, auth_headers):
    return client.post(
        "/accounts",
        json={"name": "Bank", "type": "checking", "currency": "USD", "opening_balance": 500.0},
        headers=auth_headers,
    ).json()


def _create_category(client, auth_headers):
    return client.post(
        "/categories",
        json={"name": "Salary", "type": "income"},
        headers=auth_headers,
    ).json()


def test_create_transaction(client, auth_headers):
    account = _create_account(client, auth_headers)
    res = client.post(
        "/transactions",
        json={
            "account_id": account["id"],
            "amount": 200.0,
            "type": "income",
            "date": str(date.today()),
        },
        headers=auth_headers,
    )
    assert res.status_code == 201
    assert res.json()["amount"] == 200.0


def test_list_transactions_filter_by_account(client, auth_headers):
    account = _create_account(client, auth_headers)
    client.post(
        "/transactions",
        json={"account_id": account["id"], "amount": 100.0, "type": "expense", "date": str(date.today())},
        headers=auth_headers,
    )
    res = client.get(f"/transactions?account_id={account['id']}", headers=auth_headers)
    assert res.status_code == 200
    assert len(res.json()) == 1


def test_balance_reflects_transactions(client, auth_headers):
    account = _create_account(client, auth_headers)
    client.post(
        "/transactions",
        json={"account_id": account["id"], "amount": 300.0, "type": "income", "date": str(date.today())},
        headers=auth_headers,
    )
    client.post(
        "/transactions",
        json={"account_id": account["id"], "amount": 100.0, "type": "expense", "date": str(date.today())},
        headers=auth_headers,
    )
    res = client.get(f"/accounts/{account['id']}", headers=auth_headers)
    assert res.json()["current_balance"] == 700.0  # 500 opening + 300 income - 100 expense


def test_delete_transaction(client, auth_headers):
    account = _create_account(client, auth_headers)
    tx = client.post(
        "/transactions",
        json={"account_id": account["id"], "amount": 50.0, "type": "expense", "date": str(date.today())},
        headers=auth_headers,
    ).json()
    res = client.delete(f"/transactions/{tx['id']}", headers=auth_headers)
    assert res.status_code == 204
