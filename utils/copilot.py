import requests
import json
import time

# 全局变量存储 token
token = None

def setup():
    """通过 GitHub Device Flow 获取 OAuth access token"""
    # 请求设备码和用户码
    resp = requests.post(
        "https://github.com/login/device/code",
        headers={
            "accept": "application/json",
            "editor-version": "Neovim/0.6.1",
            "editor-plugin-version": "copilot.vim/1.16.0",
            "content-type": "application/json",
            "user-agent": "GithubCopilot/1.155.0",
            "accept-encoding": "gzip,deflate,br",
        },
        json={"client_id": "Iv1.b507a08c87ecfe98", "scope": "read:user"},
    )
    resp_json = resp.json()
    device_code = resp_json.get("device_code")
    user_code = resp_json.get("user_code")
    verification_uri = resp_json.get("verification_uri")

    print(f"请访问 {verification_uri} 并输入代码 {user_code} 完成认证。")

    # 轮询获取 access token
    while True:
        time.sleep(5)
        resp = requests.post(
            "https://github.com/login/oauth/access_token",
            headers={
                "accept": "application/json",
                "content-type": "application/json",
                "user-agent": "GithubCopilot/1.155.0",
            },
            json={
                "client_id": "Iv1.b507a08c87ecfe98",
                "device_code": device_code,
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            },
        )
        resp_json = resp.json()
        access_token = resp_json.get("access_token")
        if access_token:
            print("认证成功！")
            return access_token

def get_copilot_token(access_token):
    """使用 access token 获取 Copilot token"""
    resp = requests.get(
        "https://api.github.com/copilot_internal/v2/token",
        headers={
            "authorization": f"token {access_token}",
            "editor-version": "Neovim/0.6.1",
            "editor-plugin-version": "copilot.vim/1.16.0",
            "user-agent": "GithubCopilot/1.155.0",
        },
    )
    resp_json = resp.json()
    return resp_json.get("token")

def copilot_chat(prompt):
    """调用 Copilot Chat 接口获取结果"""
    global token
    if token is None:
        access_token = setup()
        token = get_copilot_token(access_token)

    # 调用 Copilot Chat 的非官方端点（基于逆向工程）
    resp = requests.post(
        "https://copilot-proxy.githubusercontent.com/v1/chat/completions",
        headers={
            "authorization": f"Bearer {token}",
            "content-type": "application/json",
            "user-agent": "GithubCopilot/1.155.0",
        },
        json={
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "model": "gpt-4",  # Copilot Chat 可能使用的模型，未公开
            "max_tokens": 1000,
            "temperature": 0.7,
            "top_p": 1,
            "stream": False,  # 可改为 True 使用流式响应
        },
    )

    if resp.status_code != 200:
        print(f"请求失败：{resp.text}")
        return None

    resp_json = resp.json()
    return resp_json.get("choices", [{}])[0].get("message", {}).get("content", "")

def handle_request(prompt):
    """模拟 HTTP 请求处理，返回 Chat 结果"""
    result = copilot_chat(prompt)
    return result if result else "无响应"

# 测试代码
if __name__ == "__main__":
    # 示例请求
    prompt = "如何用 Python 写一个简单的 Web 服务器？"
    response = handle_request(prompt)
    print("Copilot Chat 响应：")
    print(response)