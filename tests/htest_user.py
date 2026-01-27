
from api import auth_api

def test_user_index(login_token):
    resp = get_user_index(login_token)
    result = resp.json()

    assert resp.status_code == 200
    assert result["errno"] == 0
