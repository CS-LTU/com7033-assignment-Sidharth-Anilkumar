def login(client):
    client.post("/register", data={
        "email": "admin@test.com",
        "password": "password123"
    })
    client.post("/login", data={
        "email": "admin@test.com",
        "password": "password123"
    })


def test_delete_dataset(client):
    login(client)

    response = client.post("/delete-dataset", follow_redirects=True)
    assert response.status_code == 200
