import subprocess
import sys
import os
import time
import base64
import hashlib
import hmac
import unicodedata        
import requests
import rich
import selenium
import chromedriver_autoinstaller

from rich import print
from rich import box
from rich.console import Console
from rich.columns import Columns
from rich.table import Table
console = Console()

from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

def main():
    URL = "https://smartstore.naver.com/ooooofish"
    count = 0
    
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36")
    options.add_argument("app-version=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36")
    
    while True:
        proxy_server = get_proxy().split("/")
        options.add_argument(f"--proxy-server={proxy_server[0].lower()}://{proxy_server[1]}")
        console.log(f"[{proxy_server[0]}] Proxy 할당 완료 ({proxy_server[1]})")
        
        try:
            driver = webdriver.Chrome(executable_path='chromedriver',options=options)
            driver.get(URL)
            element = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.ID, "content")))
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            console.log(f"[@] Request Succeddful.")
        except Exception as e:
            console.log("[!] Proxy Conn Failure.")
            console.log(e)
        
        driver.delete_all_cookies()
        driver.quit()
    return 0
    
def get_proxy():
    response = requests.get("https://www.proxyscan.io/api/proxy?Type=http,https&ping=100&last_check=1800")
    res_json = response.json()
    return f"{res_json[0]['Type'][0]}/{res_json[0]['Ip']}:{str(res_json[0]['Port'])}"

if __name__ == "__main__":
    try:
        chromedriver_autoinstaller.install() 
        main()
    except Exception as ex:
        if(ex == KeyboardInterrupt):
            exit(0)
        else:
            print('오류가 발생 했습니다', ex)