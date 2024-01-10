import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
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

def is_element_visible(driver, element_xpath):
    try:
        visible = driver.execute_script(
            "var elem = document.evaluate(arguments[0], document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; return (elem != null) && (elem.offsetWidth > 0 || elem.offsetHeight > 0);",
            element_xpath)
        return visible
    except:
        return False

def get_latest_response(driver):
    max_attempts = 60
    attempt = 0

    button_xpath = "//*[@data-testid='send-button']"
    response_xpath = "//*[@class='markdown prose w-full break-words dark:prose-invert dark']"
    
    time.sleep(7)

    while attempt < max_attempts:
        if is_element_visible(driver, button_xpath):
            time.sleep(1)
            responses = driver.find_elements(By.XPATH, response_xpath)
            print(f"Attempt {attempt + 1} of {max_attempts}: Waiting for the button to become visible again.")
            return responses[-1].text if responses else "응답 오류야. 알겠어?"
        else:
            time.sleep(1)
            attempt += 1

    return "응답 오류야. 알겠어?"
