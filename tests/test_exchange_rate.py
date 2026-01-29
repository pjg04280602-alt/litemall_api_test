import requests
import pytest


def test_wise_exchange_rate():
    """获取 Wise 汇率并作为测试项执行"""
    url = "https://wise.com/web-api/v1/rates"
    params = {"source": "MYR", "target": "CNY"}
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, params=params, headers=headers)
    assert response.status_code == 200

    rate_data = response.json()[0]
    rate = rate_data['rate']

    # 将汇率打印出来，方便在日志查看
    print(f"\n当前汇率: 1 MYR = {rate} CNY")

    # 也可以把汇率存入一个临时文件，方便下一步的邮件脚本读取
    with open("rate_value.txt", "w") as f:
        f.write(str(rate))

    assert rate > 0  # 基本逻辑检查