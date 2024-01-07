import requests
import os

def download_model_if_not_exists(url, local_path):
    if os.path.exists(local_path):
        return "모델 파일이 있습니다."

    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    print("모델을 다운로드합니다. 잠시만 기다려 주세요.")
    response = requests.get(url)
    with open(local_path, 'wb') as file:
        file.write(response.content)

    return f"모델 저장됨: {local_path}"
