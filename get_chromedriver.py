import os
import chromedriver_autoinstaller as AutoChrome
import shutil

def chromedriver_update():
    chrome_ver = AutoChrome.get_chrome_version().split('.')[0]

    current_list = os.listdir(os.getcwd())
    chrome_list = []
    for i in current_list:
        path = os.path.join(os.getcwd(), i)
        if os.path.isdir(path):
            if 'chromedriver.exe' in os.listdir(path):
                chrome_list.append(i)

    old_version = list(set(chrome_list)-set([chrome_ver]))

    for i in old_version:
        path = os.path.join(os.getcwd(),i)
        shutil.rmtree(path)

    if not chrome_ver in current_list:
        AutoChrome.install(True)
    else:
        pass
