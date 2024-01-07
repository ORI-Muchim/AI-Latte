import requests
import os
from tqdm import tqdm

def download_model_if_not_exists(url, local_path):
    if os.path.exists(local_path):
        return "모델 파일이 있습니다."

    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    print("모델을 다운로드합니다. 잠시만 기다려 주세요.")
    response = requests.get(url, stream=True)
    
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    
    with open(local_path, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()

    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("ERROR, something went wrong")
    return f"모델 저장됨: {local_path}"
