import pytest
import requests

from api import auth_api  # 导入业务模块

def test_user_index_with_invalid_token():
    headers = {"X-Litemall-Token": "expired-token"}
    resp = requests.get(
        "https://litemall.hogwarts.ceshiren.com/wx/user/index",
        headers=headers
    )
    result = resp.json()
    assert result["errno"] != 0

def test_login_incorrect_password():
    resp = auth_api.login("user123", "user1233")
    assert resp.json()["errno"] == 700

@pytest.mark.parametrize("username,password", [("", "123"), ("user", "")])
def test_login_param_missing(username, password):
    resp = auth_api.login(username, password)
    assert resp.json()["errno"] != 0

# 1. 测试登录本身（不需要 token 固件，因为它就在测试登录流程）
def test_login_success():
    resp = auth_api.login("user123", "user123")
    result = resp.json()
    assert result["errno"] == 0  # 断言业务状态码为 0（成功）
    assert "token" in result["data"] # 断言返回了 token

# 2. 测试获取个人中心（需要 login_token 固件）
def test_user_index(login_token):
    # 只要参数里写了 login_token，pytest 就会先运行 conftest 里的登录注入逻辑
    resp = auth_api.get_user_index()
    assert resp.json()["errno"] == 0

# 3. 测试获取订单列表
def test_order_list_success(login_token):
    resp = auth_api.get_order_list(showType=0)
    assert resp.json()["errno"] == 0

# 4. 测试手动注销接口
def test_z_logout_success(login_token):
    # 这个用例会主动调用注销，验证注销功能是否正常
    resp = auth_api.logout()
    assert resp.json()["errno"] == 0