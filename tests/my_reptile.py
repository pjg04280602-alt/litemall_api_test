import requests
import pandas as pd


def start_admin_spider():
    # 1. 确保是后台管理接口
    url = "https://litemall.hogwarts.ceshiren.com/admin/goods/list"

    # 【注意】请务必在这里填入你从浏览器复制的 Token
    # 已经为你加入了 strip() 来清理可能存在的换行或空格，防止 latin-1 报错
    raw_token = "9ceec906-d488-4dbe-acbc-79e8718f8d3c"
    my_token = raw_token.strip()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "X-Litemall-Admin-Token": my_token,
        "Accept": "application/json, text/plain, */*"
    }

    params = {
        "page": 1,
        "limit": 20,
        "sort": "add_time",
        "order": "desc"
    }

    try:
        print("🔍 正在请求后台接口获取【在售/未售】全量数据...")
        response = requests.get(url, params=params, headers=headers, timeout=10)

        if response.status_code == 401:
            print("❌ 身份验证失败：Token 无效或已过期，请重新获取。")
            return

        res_data = response.json()
        items = res_data.get('data', {}).get('list', [])

        if not items:
            print("📝 列表为空。请确认 Token 权限或页面是否有数据。")
            return

        all_results = []
        for i in items:
            # 获取布尔值（后台接口中 true 为在售，false 为未售）
            is_on_sale = i.get('isOnSale')

            # 这里的 Key 名必须和下方 df[[...]] 里的内容完全一致
            all_results.append({
                "商品ID": i.get('id'),
                "商品名称": i.get('name'),
                "接口原始值": is_on_sale,  # 👈 统一为这个名称
                "判定状态": "在售" if is_on_sale else "未售"
            })

        # 4. 展示结果
        df = pd.DataFrame(all_results)

        print("\n" + "=" * 60)
        print("📊 成功！后台商品清单如下：")
        print("-" * 60)
        # 确保这里的 ['接口原始值'] 在上面 append 的字典里确实存在
        print(df[['商品ID', '商品名称', '接口原始值', '判定状态']].head(20))
        print("=" * 60)

    except Exception as e:
        print(f"💥 运行崩溃: {e}")


if __name__ == "__main__":
    start_admin_spider()