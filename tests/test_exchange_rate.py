import requests
import os


def get_wise_rate():
    # --- 方案 A: Wise 官方接口 ---
    url_a = "https://wise.com/web-api/v1/rates"
    params = {"source": "MYR", "target": "CNY"}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Referer": "https://wise.com/zh-cn/currency-converter/myr-to-cny-rate"
    }

    try:
        print("正在尝试从 Wise 获取汇率...")
        resp = requests.get(url_a, params=params, headers=headers, timeout=10)
        if resp.status_code == 200:
            rate = resp.json()[0]['rate']
            print(f"Wise 接口调用成功: {rate}")
            return rate
        else:
            print(f"Wise 接口失效，状态码: {resp.status_code}")
    except Exception as e:
        print(f"Wise 接口请求异常: {e}")

    # --- 方案 B: 备用公开接口 (无需 Header，极度稳定) ---
    # 这是 fallback 方案，确保邮件永远不会显示“未知”
    url_b = "https://api.exchangerate-api.com/v4/latest/MYR"
    try:
        print("切换至备用公开接口...")
        resp = requests.get(url_b, timeout=10)
        if resp.status_code == 200:
            rate = resp.json()['rates']['CNY']
            print(f"备用接口调用成功: {rate}")
            return rate
    except Exception as e:
        print(f"所有接口均已失效: {e}")

    return None


def test_wise_exchange_rate():
    """Pytest 测试项"""
    rate = get_wise_rate()

    # 只要有一个接口通了，测试就通过
    assert rate is not None, "无法从任何接口获取汇率数据"
    assert rate > 0

    # 将结果写入文件，供 GitHub Actions 邮件步骤读取
    with open("rate_value.txt", "w") as f:
        f.write(str(rate))

    print(f"\n今日汇率确认: 1 MYR = {rate} CNY")


if __name__ == "__main__":
    # 方便你直接在 PyCharm 点击绿色箭头运行调试
    result = get_wise_rate()
    print(f"本地调试结果: {result}")