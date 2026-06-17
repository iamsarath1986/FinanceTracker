from datetime import date


def _create_category(client, auth_headers):
    return client.post(
        "/categories",
        json={"name": "Food", "type": "expense"},
        headers=auth_headers,
    ).json()


def _create_account(client, auth_headers):
    return client.post(
        "/accounts",
        json={"name": "Bank", "type": "checking", "currency": "USD", "opening_balance": 1000.0},
        headers=auth_headers,
    ).json()


def test_create_budget(client, auth_headers):
    category = _create_category(client, auth_headers)
    res = client.post(
        "/budgets",
        json={
            "name": "Food Budget",
            "scope_type": "category",
            "period_type": "monthly",
            "category_id": category["id"],
            "year": date.today().year,
            "month": date.today().month,
            "limit_amount": 500.0,
            "currency": "USD",
        },
        headers=auth_headers,
    )
    assert res.status_code == 201
    data = res.json()
    assert data["name"] == "Food Budget"
    assert data["spent"] == 0.0


def test_budget_spent_reflects_transactions(client, auth_headers):
    category = _create_category(client, auth_headers)
    account = _create_account(client, auth_headers)
    budget = client.post(
        "/budgets",
        json={
            "name": "Food Budget",
            "scope_type": "category",
            "period_type": "monthly",
            "category_id": category["id"],
            "year": date.today().year,
            "month": date.today().month,
            "limit_amount": 500.0,
            "currency": "USD",
        },
        headers=auth_headers,
    ).json()

    client.post(
        "/transactions",
        json={
            "account_id": account["id"],
            "category_id": category["id"],
            "amount": 120.0,
            "type": "expense",
            "date": str(date.today()),
        },
        headers=auth_headers,
    )

    res = client.get(f"/budgets/{budget['id']}", headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["spent"] == 120.0


def test_delete_budget(client, auth_headers):
    category = _create_category(client, auth_headers)
    budget = client.post(
        "/budgets",
        json={
            "name": "Test",
            "scope_type": "category",
            "period_type": "annual",
            "category_id": category["id"],
            "year": 2026,
            "limit_amount": 1000.0,
            "currency": "EUR",
        },
        headers=auth_headers,
    ).json()
    res = client.delete(f"/budgets/{budget['id']}", headers=auth_headers)
    assert res.status_code == 204
