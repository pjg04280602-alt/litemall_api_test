import json
from requests.models import Response


def mock_response(status=200, body=None):
    resp = Response()
    resp.status_code = status
    resp._content = json.dumps(body or {}).encode("utf-8")
    return resp


def mock_login():
    return mock_response(200, {
        "errno": 0,
        "data": {
            "token": "mock-token-123"
        }
    })


def mock_user_index():
    return mock_response(200, {
        "errno": 0,
        "data": {
            "nickname": "mock_user"
        }
    })


def mock_order_list():
    return mock_response(200, {
        "errno": 0,
        "data": {
            "list": []
        }
    })


def mock_logout():
    return mock_response(200, {
        "errno": 0,
        "errmsg": "成功"
    })


MOCK_RESPONSES = {
    ("POST", "/wx/auth/login"): mock_login,
    ("GET", "/wx/user/index"): mock_user_index,
    ("GET", "/wx/order/list"): mock_order_list,
    ("POST", "/wx/auth/logout"): mock_logout,
}
