import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

def start_chat_gpt(driver):
    print('물리 API에 연결합니다. 권라떼 채팅칸이 뜨면 OpenAI에 로그인해주세요.')
    driver.execute_script('''window.open("http:chat.openai.com/","_blank");''') # open page in new tab
    time.sleep(2)
    driver.switch_to.window(window_name=driver.window_handles[0])   # switch to first tab
    driver.close()
    driver.switch_to.window(window_name=driver.window_handles[0] )  # switch back to new tab
    time.sleep(2)
    driver.get("https://chat.openai.com/g/g-qGgoLD0GS-gweonradde") # this should pass cloudflare captchas now

def send_message(driver, message):
    try:
        textarea = driver.find_element(By.ID, "prompt-textarea")
        textarea.send_keys(message + Keys.ENTER)
    except NoSuchElementException:
        print("ChatGPT에 로그인 되어있지 같습니다. 프로그램 종료 후 다시 시도하세요.")
        driver.quit()

def get_latest_response(driver):
    try:
        time.sleep(16)
        responses = driver.find_elements(By.CSS_SELECTOR, ".markdown.prose.w-full.break-words.dark\\:prose-invert.dark")
        return responses[-1].text if responses else None
    except Exception as e:
        print(f"Error getting latest response: {e}")
        return None
