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
    URL = "https://cr3.shopping.naver.com/bridge/searchGate?query=%EB%B0%98%EA%B1%B4%EC%A1%B0%EC%83%9D%EC%84%A0+%EB%AA%A8%EC%9D%8C&bt=-1&nv_mid=83193516581&cat_id=50004694&h=eab9d2a61eca0e4651fa80f8a1962bff3d7f938e&t=L14D5IAV&frm=NVSCPRO"
    Referer = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EC%86%8D%EC%B4%88%EC%98%A4%EB%AF%B8%EC%9E%90&oquery=%EC%86%8D%EC%B4%88%EC%98%A4%EB%AF%B8%EC%A0%80&tqi=hlUfndprvh8ssaZV8PCssssstCs-322620"
    
    options = Options()
    
    while True:
        proxy_server = get_proxy_local("./proxy_scraper/proxies").split("|")
        console.log(f"[{proxy_server[0].upper()}] Proxy 할당 완료 ({proxy_server[1]})")
        
        try:
            sp = subprocess.Popen(getChromeDir() + r' --remote-debugging-port='+str(debugging_port)+' --user-data-dir="C:\chrometemp('+str(debugging_port)+')" --incognito --enable-auto-reload --headless' 
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
            if not refresh(driver):
                raise Exception('SearchGate Page load timeout')
            
            if not refresh_store(driver):
                raise Exception('Page load timeout')
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') #스크롤을 아래로 내림
            console.log("[>] [green bold]Proxy 접속 성공.[/green bold] 카테고리 페이지 이동 대기")
            time.sleep(10) #10초 기다리기
            driver.execute_script('window.scrollTo(document.body.scrollHeight, 0);') #스크롤을 위로 올림
            
            driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div[1]/div/div[2]/div/div/div/div/div/div[1]/div/ul[1]/li[2]/a').click() #카테고리 1번 클릭
            if not refresh_store(driver):
                raise Exception('Page load timeout')
            console.log("[>] [green bold]Proxy 접속 성공.[/green bold] 메인로고(1) 페이지 이동 대기")
            time.sleep(10) #10초 기다리기
            
            element_logo = driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div[1]/div/div[1]/h1')  #로고 클릭
            hover = ActionChains(driver).move_to_element(element_logo)
            hover.perform()
            time.sleep(2)
            element_logo.click()
            if not refresh_store(driver):
                raise Exception('Page load timeout')
            console.log("[>] [green bold]Proxy 접속 성공.[/green bold] 메인로고(2) 페이지 이동 대기")
            time.sleep(10) #10초 기다리기
            
            element_logo = driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div[1]/div/div[1]/h1')
            hover = ActionChains(driver).move_to_element(element_logo)
            hover.perform()
            time.sleep(2)
            element_logo.click()
            if not refresh_store(driver):
                raise Exception('Page load timeout')
            console.log("[>] [green bold]Proxy 접속 성공.[/green bold] 메인로고(3) 페이지 이동 대기")
            time.sleep(10) #10초 기다리기
            
            element_logo = driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div[1]/div/div[1]/h1')
            hover = ActionChains(driver).move_to_element(element_logo)
            hover.perform()
            time.sleep(2)
            element_logo.click()
            if not refresh_store(driver):
                raise Exception('Page load timeout')
            console.log("[>] [green bold]Proxy 접속 성공.[/green bold]")
            console.log("[>] 루틴 수행 완료. 10초 대기")
            time.sleep(10) #10초 기다리기
            
            today_count_tmp = driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div[1]/div/div[1]/div[2]/div/div/div/div/div/div/span[1]/em').get_attribute('innerText')
            today_count = "알수없음" if int(today_count_tmp) == 0 else today_count_tmp
            console.log(f"[@] [magenta]NStore Count = [bold]{today_count}[/bold][/magenta]")
            console.log(f"[@] [green bold]Request Successful.[/green bold]")
            
        except Exception as e:
            console.log("[!] [red]Proxy Conn Failure.[/red]")
            if e != "":
                console.log(e)
        
        driver.delete_all_cookies() #쿠키 모두 삭제
        driver.quit() #드라이버 종료
        os.kill(sp.pid, signal.SIGTERM) #크롬에 킬 신호 전송
        
        try:
            shutil.rmtree(r"c:\chrometemp("+str(debugging_port)+")", ignore_errors=True) #크롬 임시데이터 강제청소
        except FileNotFoundError:
            pass
    return 0

def get_proxy_scrap(): #웹에서 프록시 리스트 가져옴
    response = requests.get("https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt")
    res_text = response.text.split('\n')
    return f"HTTPS|{random.choice(res_text)}"  
    
def get_proxy_local(path_dir): #로컬경로에서 프록시 리스트 가져옴
    lines = list()
    file_list = os.listdir(path_dir)
    for dir_file in file_list:
        f = open(path_dir + '/' + dir_file,'r')
        lines = lines + f.readlines()
        f.close()
    ln = random.choice(lines).strip()
    type_proxy = ln.split(':')[0]
    return f"{type_proxy}|{ln}"  

def get_proxy_socket(path_socket4, path_socket5): #Socket4/5 Proxy만 가져옴
    f1 = open(path_socket4, 'r')
    f2 = open(path_socket5, 'r')
    lines = f1.readlines() + f2.readlines()
    f1.close()
    f2.close()
    return f"SOCKET|{random.choice(lines).strip()}"   

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
    
def refresh(driver):
    loop = 0
    while True:
        loop = loop + 1
        if loop > 10: #10번 재시도 후 변화 없으면 false 리턴
            return False
        try:
            element = WebDriverWait(driver, 5).until(
                lambda wd: True if driver.current_url.find("smartstore.naver.com") != -1 else False
            )
            return True
        except Exception as e:
            console.log("["+str(loop)+"/10]"+" [green bold]Refresh[/green bold] 프록시 연결시간 초과. Refresh 명령 전송")
            driver.refresh()

def refresh_store(driver): #스토어 내부에서 새로고침
    loop = 0
    while True:
        loop = loop + 1
        if loop > 3: #3번 재시도 후 변화 없으면 False 리턴
            return False
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "MAIN_CONTENT_ROOT_ID"))
            )
            return True
        except Exception as e:
            console.log("["+str(loop)+"/3]" +" [green bold]Store Refresh[/green bold] 프록시 연결시간 초과. Refresh 명령 전송")
            driver.refresh()
    
if __name__ == "__main__":
    console.log("[!] DEBUG PORT = " + str(debugging_port))
    signal.signal(signal.SIGINT, sigint_handler)
    try:
        chromedriver_autoinstaller.install() 
        main()
    except Exception as ex:
        console.log("[bold][red][Important][/red][/bold] 처리되지 않은 오류가 발생했습니다.")
        console.log(ex)
        exit(0)
