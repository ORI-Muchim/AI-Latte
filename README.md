# AI-LATTE

# The repository is only accessible to people aged 19 and over. *PLEASE DO NOT CHECK* the repository for teenagers or children.

[한국어 README.md](./README_Korean.md)

Onfire Games's Love Delivery Heroine Latte, An Unofficial Implementation of [ChatGPT](https://chat.openai.com/) and [MB-iSTFT-VITS](https://github.com/ORI-Muchim/MB-iSTFT-VITS-Korean)

![Sample Output](./src/1.png)

## Table of Contents 
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [References](#references)

## Prerequisites
- **ChatGPT4**
- A Windows / Linux / MacOS system with a minimum of `8GB` RAM.
- Python == 3.8
- Anaconda installed.
- PyTorch installed.

Pytorch install command(For CUDA user):
```sh
pip install torch==1.13.1+cu117 torchvision==0.14.1+cu117 torchaudio==0.13.1 --extra-index-url https://download.pytorch.org/whl/cu117
```

Pytorch install command(For CPU user):
```sh
pip install torch==1.13.1+cpu torchvision==0.14.1+cpu torchaudio==0.13.1 --extra-index-url https://download.pytorch.org/whl/cpu
```

---

## Installation 
1. **Create an Anaconda environment:**

```sh
conda create -n latte python=3.8
```

2. **Activate the environment:**

```sh
conda activate latte
```

3. **Clone this repository to your local machine:**

```sh
git clone https://github.com/ORI-Muchim/AI-LATTE.git
```

4. **Navigate to the cloned directory:**

```sh
cd AI-LATTE
```

5. **Install the necessary dependencies:**

```sh
pip install -r requirements.txt
```

---

## Usage

To start this application, use the following command:

```sh
python app.py
```

---
## References

For more information, please refer to the following repositories: 
- [MasayaKawamura/MB-iSTFT-VITS](https://github.com/MasayaKawamura/MB-iSTFT-VITS) 
- [ORI-Muchim/MB-iSTFT-VITS-Korean](https://github.com/ORI-Muchim/MB-iSTFT-VITS-Korean)
- [ORI-Muchim/PolyLangVITS](https://github.com/ORI-Muchim/PolyLangVITS)
- [tenebo/g2pk2](https://github.com/tenebo/g2pk2)

This project reveals that it was not created for commercial purposes, but for simple research purposes.