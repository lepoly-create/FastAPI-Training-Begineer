from fastapi.testclient import TestClient


def test_home(client: TestClient) -> None:

    response = client.get("/")
    ##assert permet de s'assurer que la condition qui lui suit est vrai
    assert response.status_code == 200
    assert "Current url" in response.text

