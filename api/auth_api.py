from api.base_request import base  # 导入上面那个已经实例化的 base 对象

def get_user_index():
    """获取用户信息：内部自动调用 base.get，并自动带上 token"""
    return base.get("/wx/user/index")

def login(username, password):
    """登录接口：将用户名密码转为 JSON 发送"""
    return base.post("/wx/auth/login", json={"username": username, "password": password})

def logout():
    """注销接口：直接调用 post，base 会自动处理 Header 里的 Token"""
    return base.post("/wx/auth/logout")

def get_order_list(showType=0):
    """获取订单列表：params 会将参数拼接成 ?showType=0"""
    return base.get("/wx/order/list", params={"showType": showType})

def get_catalog_current(catalog_id):
    """获取分类详情：传入分类 ID"""
    return base.get("/wx/catalog/current", params={"id": catalog_id})