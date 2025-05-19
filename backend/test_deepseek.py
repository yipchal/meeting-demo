import requests

# ✅ 替换为你自己的 DeepSeek API Key
API_KEY = "sk-3d5b936e130a4e6aad280e3e276ea8d7"

def test_deepseek():
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是一个助手"},
            {"role": "user", "content": "请用一句话介绍你自己"}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        print("📡 状态码：", response.status_code)

        if response.status_code == 200:
            result = response.json()
            message = result["choices"][0]["message"]["content"]
            print("✅ 返回内容：\n", message)
        else:
            print("❌ 请求失败：", response.text)
    except Exception as e:
        print("🚨 出错：", e)

if __name__ == "__main__":
    test_deepseek()
