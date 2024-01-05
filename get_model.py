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
