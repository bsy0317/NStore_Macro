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

from rich import print
from rich import box
from rich.console import Console
from rich.columns import Columns
from rich.table import Table
console = Console()

def main():
    URL = "https://smartstore.naver.com/ooooofish/products/5649019336"
    request_headers = {'User-Agent' : ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/605.1.15\
    (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/605.1.15'),
    'Referer': 'https://cr.shopping.naver.com/adcr.nhn?x=5xgk0o%2FxXFpmUSEqnZiMAf%2F%2F%2Fw%3D%3Ds%2BCWfv631H6tObR52AEQQDt6jWWebTbkeJHb44kZ52rMGpuC4VbNVyxN%2BtJ0rLKH0OCkyosZuN3LkYlnxTdBJ7ZjQgYbrZL9aR%2FDkx82JiD1IMvbPuiP%2FjrRXSeOxXFWL0X90L1ljkAEVSjmStAe999kzUcfthzKjbftAcC5CTHPvbFbCHc5MwHtep5oytzJblFkJv7%2FGg8vgWY87RMjS3jlrq1uM7bPAMzmOluPP7EtD4P%2Bj2CVvS6QkrpszyaIo6sGkobrHOLjdQ9PfNparAPguzbdcNHkPsAELGL7l%2F50fi1cp%2B8QtYpmHeRMAbPQhE4Dx5kATpPTRMEyS1hVWyMmscUZuB%2FB3GA4tAdwd4kJn0E%2B7lsL8Xc%2FJzL4VwihdN00CswaTs22ObTnm4j0ulljCt58qbD%2BRfesCX7ikynyi4%2Fr0lz1oSk9AW8qzFsUvpOr9sPYwajBkeE07IGGkJ5SCPsmGKllbt0kl8XIxCXSaW9%2B2TdBqLfvUrowSfyGYWLZaZga65DYcSsOcEod%2B70xsS3tSAApU8%2F60dhmqvG4ZIonLZYIZnUXNxdOrUDQzs586Lq5uuwnPH0HpXU3Joto7MmLwgspaDMrKjkxnlIbAkjdKbZ0ldlv%2FmgNh%2B4NIpq0hLmtxqBcD3Jax19oBLL8KMQ5XVUesE3eI%2FTjQDVrWDLsEKMWwV8kWkvfATCkeB3JWD2w80rMEju2mDPG8o%2BvM3s8AGAYQEMSVntmJzwBtsTjGrOlp0XPMI1xP90YRgRA2fGaKe9voP9GEohFgtnySN8h8%2FaZOQGyCkSmLkMZMgRMcs3KzajSOCbGpFQmo8bqU4650%2BGkhpOfxP7ZIIYu5mW8mvZFd3nEYzo3VOiSQ%2BMQQRSuVrpKm8ndhhZzDQdAiJdwXirBRdnaxfvrBbw%3D%3D&nvMid=83193516581&catId=50004694'}
    count = 0
    while True:
        proxy_server = get_proxy().split("/")
        proxies = {"TYPE":"HOST:PORT"}
        if proxy_server[0] == "HTTP":
            proxies = {"http": proxy_server[1]}
        elif proxy_server[0] == "HTTPS":
            proxies = {"https": proxy_server[1]}
        console.log(f"[{proxy_server[0]}] Proxy 할당 완료 ({proxy_server[1]})")
        
        try:
            resp = requests.get(URL, headers=request_headers, proxies=proxies, timeout=10)
            console.log(f"[@] Request Succeddful. StatusCode({resp.status_code})")
            txt= resp.text
        except Exception as e:
            console.log("[!] Proxy Conn Failure.")
            console.log(e)
        time.sleep(2)
        
    return 0
    
def get_proxy():
    response = requests.get("https://www.proxyscan.io/api/proxy?level=elite&Type=http,https&ping=200&last_check=3600")
    res_json = response.json()
    return f"{res_json[0]['Type'][0]}/{res_json[0]['Ip']}:{str(res_json[0]['Port'])}"

if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        if(ex == KeyboardInterrupt):
            exit(0)
        else:
            print('오류가 발생 했습니다', ex)