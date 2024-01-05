import requests
import os

def download_file_if_not_exists(url, local_path):
    if os.path.exists(local_path):
        return "모델 있음. 다운로드 건너뜀."

    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    response = requests.get(url)
    with open(local_path, 'wb') as file:
        file.write(response.content)

    return f"모델 저장됨: {local_path}"

url = 'https://github.com/ORI-Muchim/AI-Latte/releases/download/v1.0/G_107000.pth'

local_path = './models/latte/G_107000.pth'

result = download_file_if_not_exists(url, local_path)
print(result)
