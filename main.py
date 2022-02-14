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
debugging_port = random.randrange(60000,65000)

def main():
    URL = "https://cr3.shopping.naver.com/bridge/searchGate?query=%EC%86%8D%EC%B4%88%EC%98%A4%EB%AF%B8%EC%9E%90+%EB%B0%98%EA%B1%B4%EC%A1%B0%EC%83%9D%EC%84%A0&bt=-1&nv_mid=83193516581&cat_id=50004694&h=39e475322b0aaa367d1d93b79773f0f3f08fc916&t=KZM29POQ&frm=NVSCPRO"
    Referer = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EC%86%8D%EC%B4%88%EC%98%A4%EB%AF%B8%EC%9E%90&oquery=%EC%86%8D%EC%B4%88%EC%98%A4%EB%AF%B8%EC%A0%80&tqi=hlUfndprvh8ssaZV8PCssssstCs-322620"
    
    options = Options()
    options.add_argument('headless')
    
    while True:
        proxy_server = get_proxy_3().split("/") #2번 프록시 Parser 사용
        console.log(f"[{proxy_server[0]}] Proxy 할당 완료 ({proxy_server[1]})")
        
        try:
            sp = subprocess.Popen(getChromeDir() + r' --remote-debugging-port='+str(debugging_port)+' --user-data-dir="C:\chrometemp('+str(debugging_port)+')" --incognito --window-size=1024,768' 
            + f" --proxy-server={proxy_server[1]}") # 디버거 크롬 구동(Headless, 익명모드, 프록시)
            kill_pid_backup = sp.pid
            options.add_experimental_option("debuggerAddress", f"127.0.0.1:{debugging_port}") #크롬 디버깅포트 연결
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
            console.log("[>] [green bold]Proxy 접속 성공.[/green bold] 카테고리 페이지 이동 대기")
            time.sleep(10) #10초 기다리기
            
            driver.execute_script('window.scrollTo(document.body.scrollHeight, 0);') #스크롤을 위로 올림
            driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div[1]/div/div[2]/div/div/div/div/div/div[1]/div/ul[1]/li[2]/a').click() #카테고리 1번 클릭
            element = WebDriverWait(driver,60).until(EC.presence_of_element_located((By.ID, "MAIN_CONTENT_ROOT_ID"))) #로딩완료될때 까지 기다림(제한시간 1분)
            console.log("[>] [green bold]Proxy 접속 성공.[/green bold] 메인로고(1) 페이지 이동 대기")
            time.sleep(10) #10초 기다리기
            
            element_logo = driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div[1]/div/div[1]/h1')  #로고 클릭
            hover = ActionChains(driver).move_to_element(element_logo)
            hover.perform()
            time.sleep(2)
            element_logo.click()
            element = WebDriverWait(driver,60).until(EC.presence_of_element_located((By.ID, "MAIN_CONTENT_ROOT_ID"))) #로딩완료될때 까지 기다림(제한시간 1분)
            console.log("[>] [green bold]Proxy 접속 성공.[/green bold] 메인로고(2) 페이지 이동 대기")
            time.sleep(10) #10초 기다리기
            
            element_logo = driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div[1]/div/div[1]/h1')
            hover = ActionChains(driver).move_to_element(element_logo)
            hover.perform()
            time.sleep(2)
            element_logo.click()
            element = WebDriverWait(driver,60).until(EC.presence_of_element_located((By.ID, "MAIN_CONTENT_ROOT_ID"))) #로딩완료될때 까지 기다림(제한시간 1분)
            console.log("[>] [green bold]Proxy 접속 성공.[/green bold] 메인로고(3) 페이지 이동 대기")
            time.sleep(10) #10초 기다리기
            
            element_logo = driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div[1]/div/div[1]/h1')
            hover = ActionChains(driver).move_to_element(element_logo)
            hover.perform()
            time.sleep(2)
            element_logo.click()
            element = WebDriverWait(driver,60).until(EC.presence_of_element_located((By.ID, "MAIN_CONTENT_ROOT_ID"))) #로딩완료될때 까지 기다림(제한시간 1분)
            console.log("[>] [green bold]Proxy 접속 성공.[/green bold]")
            console.log("[>] 루틴 수행 완료. 10초 대기")
            time.sleep(10) #10초 기다리기
            
            today_count_tmp = driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div[1]/div/div[1]/div[2]/div/div/div/div/div[2]/div/span[1]/em').get_attribute('innerText')
            today_count = "알수없음" if int(today_count_tmp) == 0 else today_count_tmp
            console.log(f"[@] [magenta]NStore Count = [bold]{today_count}[/bold][/magenta]")
            console.log(f"[@] [green bold]Request Successful.[/green bold]")
            
        except Exception as e:
            console.log("[!] [red]Proxy Conn Failure.[/red]")
            console.log(e)
        
        driver.delete_all_cookies() #쿠키 모두 삭제
        driver.quit() #드라이버 종료
        os.kill(sp.pid, signal.SIGTERM) #크롬에 킬 신호 전송
        
        try:
            shutil.rmtree(r"c:\chrometemp("+str(debugging_port)+")", ignore_errors=True) #크롬 임시데이터 강제청소
        except FileNotFoundError:
            pass
    return 0
    
def get_proxy_1(): #프록시 크롤링 1번
    response = requests.get("https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/json/proxies-http%2Bhttps-beautify.json")
    res_json = response.json()['https'] #HTTPS Proxy만 추출
    return f"HTTPS/{random.choice(res_json)}"
    
def get_proxy_2(): #프록시 크롤링 2번
    response = requests.get("https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt")
    res_text = response.text.split('\n')
    return f"HTTPS/{random.choice(res_text)}"  

def get_proxy_3(): #프록시 크롤링 3번
    response = requests.get("https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt")
    res_text = response.text.split('\n')
    return f"HTTPS/{random.choice(res_text)}"  

def sigint_handler(signal, frame):
    kill_all(kill_pid_backup) #크롬에 킬 신호 전송
    sys.exit(0)

def kill_all(pid):
    subprocess.Popen("TASKKILL /F /PID {pid} /T".format(pid=pid)) #크롬에 킬 신호 전송
    shutil.rmtree(r"c:\chrometemp("+str(debugging_port)+")", ignore_errors=True) #크롬 임시데이터 강제청소
    return 0

def getChromeDir():
    dir_32bit = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    dir_64bit = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    if os.path.isfile(dir_32bit):
        return dir_32bit
    else:
        return dir_64bit
    return 0

if __name__ == "__main__":
    console.log("[!] DEBUG PORT = " + str(debugging_port))
    signal.signal(signal.SIGINT, sigint_handler)
    try:
        chromedriver_autoinstaller.install() 
        main()
    except Exception as ex:
        console.log("[bold][red][Important][/red][/bold] 처리되지 않은 오류가 발생했습니다.")
        exit(0)
