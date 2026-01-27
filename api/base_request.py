# base_request.py
import requests
import logging
# 修正后的导入：确保 Sources Root 设置正确后，直接从包名开始
from config.settings import BASE_URL, USE_MOCK  #
from mock.mock_data import MOCK_RESPONSES       #


class BaseRequest:
    def __init__(self, base_url):
        self.base_url = base_url
        self.token = None  # 全局 token（单例状态）

    def set_token(self, token):
        """设置全局 Token"""
        self.token = token

    def request(self, method, url, headers=None, **kwargs):
        """所有请求的统一入口"""

        # ===================== Mock 分支 =====================
        if USE_MOCK:
            key = (method.upper(), url)
            if key in MOCK_RESPONSES:
                print(f"\n[MOCK] 命中 Mock 接口: {method} {url}")
                return MOCK_RESPONSES[key]()
            else:
                raise Exception(f"[MOCK ERROR] 未配置 Mock: {method} {url}")

        # ===================== 真接口分支 =====================
        full_url = self.base_url + url
        final_headers = {}
        if headers:
            final_headers.update(headers)

        if self.token:
            final_headers["X-Litemall-Token"] = self.token

        print(f"\n[真实请求] URL: {full_url}")
        print(f"[真实请求] Headers: {final_headers}")
        print(f"[真实请求] Params: {kwargs}")

        return requests.request(
            method=method,
            url=full_url,
            headers=final_headers,
            timeout=10,
            **kwargs
        )

    # 快捷方法
    def get(self, url, **kwargs):
        return self.request("GET", url, **kwargs)

    def post(self, url, **kwargs):
        return self.request("POST", url, **kwargs)


# ⭐ 全项目唯一 BaseRequest 实例
base = BaseRequest(BASE_URL)
