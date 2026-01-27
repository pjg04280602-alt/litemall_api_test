import pytest
from api.auth_api import base, login, logout  # 导入单例 base 和 业务函数

@pytest.fixture(scope="session")  # 设置作用域为 session，即整个测试期间只登录一次
def login_token():
    # --- 【测试开始前】 ---
    resp = login("user123", "user123")  # 先跑一遍登录
    token = resp.json()["data"]["token"] # 从返回结果提取 Token

    # ⭐ 将 Token 注入到单例 base 对象中，此时所有调用 base 的接口都变为了“已登录状态”
    base.set_token(token)
    print(f"\n[固件] Token 已注入 base 对象: {base.token[:20]}...")

    yield token  # 相当于“暂停键”，返回 token 给测试用例，开始执行 test_ 开头的函数

    # --- 【测试结束后】 ---
    # 当所有测试用例跑完，代码会回到这里执行
    logout()  # 调用注销接口，告知服务器该 Token 失效