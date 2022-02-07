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
import random
import shutil
import stat
import signal

from rich import print
from rich import box
from rich.console import Console
from rich.columns import Columns
from rich.table import Table
console = Console()

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

kill_pid_backup = 0

def main():
    URL = "https://smartstore.naver.com/ooooofish"
    #URL = "https://ipipip.kr"
    
    options = Options()
    options.add_argument('headless')
    
    while True:
        proxy_server = get_proxy_2().split("/") #2번 프록시 Parser 사용
        console.log(f"[{proxy_server[0]}] Proxy 할당 완료 ({proxy_server[1]})")
        
        try:
            sp = subprocess.Popen(r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp" --incognito --window-size=1920,1080 --headless' 
            + f" --proxy-server={proxy_server[1]}") # 디버거 크롬 구동(Headless, 익명모드, 프록시)
            kill_pid_backup = sp.pid
            options.add_experimental_option("debuggerAddress", "127.0.0.1:9222") #크롬 디버깅포트 연결
            chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0] #크롬버전 파싱(폴더경로)
            try:
                driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=options) #크롬드라이버 실행
            except:
                chromedriver_autoinstaller.install(True) #만약 없다면 업데이트
                driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=options)
            time.sleep(2) #2초 기다리기
            
            driver.get(URL) #스토어 URL 방문
            element = WebDriverWait(driver,60).until(EC.presence_of_element_located((By.ID, "MAIN_CONTENT_ROOT_ID"))) #메인페이지가 로딩완료될때 까지 기다림(제한시간 1분)
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') #스크롤을 아래로 내림
            time.sleep(10) #10초 기다리기
            
            driver.execute_script('window.scrollTo(document.body.scrollHeight, 0);') #스크롤을 위로 올림
            driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div[1]/div/div[2]/div/div/div/div/div/div[1]/div/ul[1]/li[2]/a').click() #카테고리 1번 클릭
            element = WebDriverWait(driver,60).until(EC.presence_of_element_located((By.ID, "MAIN_CONTENT_ROOT_ID"))) #로딩완료될때 까지 기다림(제한시간 1분)
            time.sleep(10) #10초 기다리기
            
            element_logo = driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div[1]/div/div[1]/h1')  #로고 클릭
            hover = ActionChains(driver).move_to_element(element_logo)
            hover.perform()
            time.sleep(1)
            element_logo.click()
            element = WebDriverWait(driver,60).until(EC.presence_of_element_located((By.ID, "MAIN_CONTENT_ROOT_ID"))) #로딩완료될때 까지 기다림(제한시간 1분)
            time.sleep(10) #10초 기다리기
            
            hover.perform()
            time.sleep(1)
            element_logo.click()
            time.sleep(10) #10초 기다리기
            
            console.log(f"[@] Request Successful.")
        except Exception as e:
            console.log("[!] Proxy Conn Failure.")
            console.log(e)
        
        driver.delete_all_cookies() #쿠키 모두 삭제
        driver.quit() #드라이버 종료
        os.kill(sp.pid, signal.SIGTERM) #크롬에 킬 신호 전송
        
        try:
            shutil.rmtree(r"c:\chrometemp", ignore_errors=True) #크롬 임시데이터 강제청소
        except FileNotFoundError:
            pass
    return 0
    
def get_proxy(): #프록시 크롤링 1번
    response = requests.get("https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/json/proxies-http%2Bhttps-beautify.json")
    res_json = response.json()['https'] #HTTPS Proxy만 추출
    return f"HTTPS/{random.choice(res_json)}"
    
def get_proxy_2(): #프록시 크롤링 2번
    response = requests.get("https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt")
    res_text = response.text.split('\n')
    return f"HTTPS/{random.choice(res_text)}"  

def sigint_handler(signal, frame):
    kill_all(kill_pid_backup) #크롬에 킬 신호 전송
    sys.exit(0)

def kill_all(pid):
    subprocess.Popen("TASKKILL /F /PID {pid} /T".format(pid=pid)) #크롬에 킬 신호 전송
    return 0
    
if __name__ == "__main__":
    signal.signal(signal.SIGINT, sigint_handler)
    try:
        chromedriver_autoinstaller.install() 
        main()
    except Exception as ex:
        exit(0)