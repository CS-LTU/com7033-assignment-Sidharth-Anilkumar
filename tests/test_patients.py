def login(client):
    client.post("/register", data={
        "email": "user@test.com",
        "password": "password123"
    })
    client.post("/login", data={
        "email": "user@test.com",
        "password": "password123"
    })


def test_add_patient(client):
    login(client)

    response = client.post("/patients/new", data={
        "external_id": 1,
        "gender": "Male",
        "age": 45,
        "hypertension": "1",
        "ever_married": "Yes",
        "work_type": "Private",
        "residence_type": "Urban",
        "avg_glucose_level": 120.5,
        "bmi": 23.4,
        "smoking_status": "never smoked",
        "stroke": "0",
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Male" in response.data
