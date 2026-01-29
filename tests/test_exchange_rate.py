import requests
import os


def get_wise_rate():
    # 方案 A: Wise 官方接口 (带上更全的 Header)
    url_a = "https://wise.com/web-api/v1/rates"
    params = {"source": "MYR", "target": "CNY"}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Referer": "https://wise.com/zh-cn/currency-converter/myr-to-cny-rate"
    }

    try:
        print("尝试从 Wise 获取汇率...")
        resp = requests.get(url_a, params=params, headers=headers, timeout=10)
        if resp.status_code == 200:
            return resp.json()[0]['rate']
        else:
            print(f"Wise 接口返回状态码: {resp.status_code}")
    except Exception as e:
        print(f"Wise 接口异常: {e}")

    # 方案 B: 备用公开接口 (无需 Header，极其稳定)
    url_b = "https://api.exchangerate-api.com/v4/latest/MYR"
    try:
        print("Wise 失败，尝试备用接口...")
        resp = requests.get(url_b, timeout=10)
        if resp.status_code == 200:
            rate = resp.json()['rates']['CNY']
            return rate
    except Exception as e:
        print(f"备用接口也异常: {e}")

    return None


def test_wise_exchange_rate():
    """这是给 Pytest 调用的测试项"""
    rate = get_wise_rate()

    # 断言汇率获取成功
    assert rate is not None, "两个接口均未能获取到汇率数据"
    assert rate > 0

    print(f"\n当前最终采用汇率: 1 MYR = {rate} CNY")

    # 写入文件供后续 Workflow 步骤读取
    with open("rate_value.txt", "w") as f:
        f.write(str(rate))


if __name__ == "__main__":
    # 本地直接 python 运行调试
    res = get_wise_rate()
    print(f"最终结果: {res}")