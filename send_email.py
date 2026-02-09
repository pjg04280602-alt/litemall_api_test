import smtplib, os, sys, requests
import xml.etree.ElementTree as ET
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def get_rate():
    """从 comparisons 接口精准提取汇率"""
    try:
        # 你提供的最新接口地址
        url = "https://wise.com/gateway/v4/comparisons"
        params = {
            "sourceCurrency": "MYR",
            "targetCurrency": "CNY",
            "sendAmount": "1000",
            "sourceCountry": "CN",
            "filter": "POPULAR",
            "includeWise": "true",
            "numberOfProviders": "3"
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Content-Type": "application/json"
        }

        r = requests.get(url, params=params, headers=headers, timeout=15)
        if r.status_code == 200:
            data = r.json()
            # 这里的解析路径对应截图：providers -> 第一个元素(Wise) -> quotes -> 第一个元素 -> rate
            providers = data.get('providers', [])
            for p in providers:
                if p.get('alias') == 'wise':
                    rate = p.get('quotes', [{}])[0].get('rate')
                    return float(rate)
    except Exception as e:
        print(f"Wise 接口解析异常: {e}")

    # 备用接口（防止主接口由于反爬策略失效）
    try:
        r = requests.get("https://api.exchangerate-api.com/v4/latest/MYR", timeout=10)
        return float(r.json()['rates']['CNY'])
    except:
        return None


def get_test_stats():
    try:
        if not os.path.exists('result.xml'): return None
        tree = ET.parse('result.xml')
        root = tree.getroot()
        ts = root if root.tag == 'testsuite' else root[0]
        total = int(ts.get('tests', 0))
        fail = int(ts.get('failures', 0))
        err = int(ts.get('errors', 0))
        skip = int(ts.get('skipped', 0))
        return {
            "total": total, "failures": fail, "time": ts.get('time', 0),
            "passed": total - fail - err - skip
        }
    except:
        return None


def send():
    raw_rate = get_rate()

    if raw_rate is not None:
        # 1. 原始汇率：保留 5 位小数 (如 1.76324)
        raw_rate_5f = "{:.5f}".format(raw_rate)
        # 2. 汇率指数：放大 1000 倍
        rate_index = raw_rate * 1000
        # 3. 指数显示：保留 2 位小数 (如 1763.24)
        rate_index_text = "{:.2f}".format(rate_index)
    else:
        raw_rate_5f = "获取失败"
        rate_index_text = "获取失败"

    stats = get_test_stats()
    sender = os.environ.get('MAIL_USER')
    msg = MIMEMultipart()

    msg['Subject'] = f"📊 测试报告 | 汇率指数: {rate_index_text}"
    msg['From'] = f"QA-Bot <{sender}>"
    msg['To'] = os.environ.get('RECEIVER')

    color = "#28a745" if stats and int(stats['failures']) == 0 else "#dc3545"
    html = f"""
              <html><body>
                <h2 style="color: {color};">测试执行完毕</h2>
                <h3 style="color: #007bff;">💱 汇率监控 (MYR -> CNY)</h3>
                <p style="font-size: 18px;">
                    <b>原始汇率 (5位): <span style="color: #6c757d;">{raw_rate_5f}</span></b><br>
                    <b>汇率指数 (x1000): <span style="color: #e83e8c; font-size: 26px;">{rate_index_text}</span></b>
                </p>
              """
    if stats:
        html += f"""
                  <h3 style="color: #007bff;">🧪 测试统计</h3>
                  <table border="1" style="border-collapse: collapse; text-align: center; width: 240px;">
                    <tr style="background-color: #f2f2f2;"><th>项目</th><th>数量</th></tr>
                    <tr><td>总用例</td><td>{stats['total']}</td></tr>
                    <tr style="color: green;"><td>通过</td><td>{stats['passed']}</td></tr>
                    <tr style="color: red;"><td>失败</td><td>{stats['failures']}</td></tr>
                  </table>
                  """
    html += "</body></html>"
    msg.attach(MIMEText(html, 'html'))

    if os.path.exists("report.html"):
        with open("report.html", "rb") as f:
            part = MIMEApplication(f.read(), Name="report.html")
            part['Content-Disposition'] = 'attachment; filename="report.html"'
            msg.attach(part)

    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(sender, os.environ.get('MAIL_PASS'))
        s.sendmail(sender, [msg['To']], msg.as_string())
        s.quit()
        print(f"发送成功！原始:{raw_rate_5f}, 指数:{rate_index_text}")
    except Exception as e:
        print(f"发送失败: {e}")


if __name__ == "__main__":
    send()