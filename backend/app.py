import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import requests

# 加载 .env 文件中的环境变量
load_dotenv()

app = Flask(__name__)
CORS(app)

# 从环境变量中获取 API 密钥
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
print(f"🔑 当前使用的 DeepSeek API Key: {DEEPSEEK_API_KEY}")


def summarize_text(content, mode="formal"):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }

    # 根据模式选择不同的 system prompt
    if mode == "funny":
        system_prompt = (
            "你是一个幽默风趣的会议总结助手，请用搞笑轻松的语气总结会议重点，"
            "吐槽废话和冗余部分，风格自由但不失重点。"
        )
    else:
        system_prompt = (
            "你是一个专业的会议纪要助手，请准确提炼会议内容的关键点，"
            "忽略无关内容，输出一份正式清晰的总结。"
        )

    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": content}
        ],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        print("❌ DeepSeek API 调用失败:", response.status_code, response.text)
        return "总结失败，请稍后再试。"


@app.route('/')
def home():
    return "Hello from Flask backend!"

@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        data = request.get_json()
        content = data.get("text", "").strip()
        mode = data.get("mode", "formal")  # 默认为正式模式

        if not content:
            return jsonify({"error": "No text provided"}), 400

        summary = summarize_text(content, mode)
        return jsonify({"summary": summary})
    except Exception as e:
        print("❌ 出错：", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
