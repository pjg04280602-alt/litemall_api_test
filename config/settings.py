# config/settings.py

# True = 用 Mock
# False = 用真实接口
USE_MOCK = False

REAL_BASE_URL = "https://litemall.hogwarts.ceshiren.com"
MOCK_BASE_URL = "http://localhost:8080"

BASE_URL = MOCK_BASE_URL if USE_MOCK else REAL_BASE_URL
