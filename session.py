import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
import random
import time
import os

import tools


class Log:
    def __init__(self, keys: list[str]):
        self.keys = keys
        self.logs = []
    def log(self, message: str):
        self.logs.append(message)
    def __str__(self):
        return "\n".join(self.logs)
    def save(self):
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        lastlogs = os.listdir(log_dir)
        lastlogs.sort()
        lastlog = lastlogs[-1] if lastlogs else "0.log"
        log_file = os.path.join(log_dir, f"{int(lastlog.split('.')[0]) + 1}.log")
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(str(self))
        print(f"Log saved to {log_file}")
        return log_file
    

class Session:
    def __init__(self, ksnplsid: str, log: Log, secrets: list[str]):
        self.created_at = time.time()
        self.renewed_at = time.time()
        self.ksnplsid = ksnplsid
        self.secrets= secrets
        self.log = log
        self.active = True
        self.log.log(f"Session created with KSNPLSID: {self.ksnplsid} at {time.ctime(self.created_at)}")
        
    def __str__(self):
        return f"Session(ksnplsid={self.ksnplsid})"
    
    def update_name(self, username: str) -> None:
        self.log.log(f">>> Updating name to: {username}")
        tools.update_name(self.ksnplsid, self.log, username)

    def upload_picture(self, pic_path: str) -> None:
        if not os.path.exists(pic_path):
            self.log.log(f"❌ Picture path does not exist: {pic_path}")
            raise FileNotFoundError(f"Picture path does not exist: {pic_path}")
        self.log.log(f">>> Uploading picture from: {pic_path}")
        tools.upload_picture(self.ksnplsid, self.log, pic_path)

    def renew(self):
        self.log.log(">>> Renewing session...")
        self.ksnplsid, self.log = dologin(self.secrets, self.log)
        if not self.ksnplsid:
            self.log.log("❌ Session renewal failed: KSNPLSID not found!")
            self.log.save()
            raise Exception("Session renewal failed: KSNPLSID not found!")
        self.log.log(">>> Session renewed successfully!")
        self.renewed_at = time.time()
        self.active = True
        return self
    
    def test(self) -> bool:
        self.log.log(">>> Testing session...")
        test_url = "https://kisnaplo.karinthy.hu/app/interface.php?view=v_k78_main&KSNPLSID=" + self.ksnplsid
        self.log.log(f">>> Sending GET request to: {test_url}")
        response = requests.get(test_url, allow_redirects=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        status = soup.find('div', id='hideMe').text.strip()
        self.log.log(f">>> Status: {status}")
        if not status.startswith("OK"):
            self.log.log("❌ Session test failed!")
            self.active = False
            return False
        self.log.log(">>> Session test successful!")
        return True

    

def get_session(password_inputs: list[str] | str) -> Session:
    password_inputs = password_inputs.strip().replace(" ", "").replace("\n", "").replace("-", "")
    if not isinstance(password_inputs, list):
        password_inputs = [password_inputs[0:4], password_inputs[4:8], password_inputs[8:12]]
    keys = password_inputs.copy()

    log = Log(keys)
    ksnplsid, log = dologin(keys, log)
    
    sesssion = Session(ksnplsid, log, keys)
    log.log(">>> Login successful! Session created.")

    return sesssion



def dologin(keys: str | list[str], log: Log) -> str:
    if not isinstance(keys, list):
        keys = [keys[0:4], keys[4:8], keys[8:12]]
    keys_login=keys.copy()

    log= Log(keys_login)
    log.log(">>> Starting login process...")

    page_url = "https://kisnaplo.karinthy.hu/app/interface.php?view=v_k78_login"

    presession = requests.Session() 
    response = presession.get(page_url)
    soup = BeautifulSoup(response.text, "html.parser")
    form1 = soup.find("form")
    if not form1:
        log.log("❌ Első form nem található")
        log.save()
        raise Exception("Első form nem található")
    action1 = form1.get("action")
    form1_url = urljoin(page_url, action1)
    inputs1 = form1.find_all("input")
    form_data1 = {}
    for tag in inputs1:
        name = tag.get("name")
        value = tag.get("value", "")
        if name:
            if not value and "password" in tag.get("type", ""):
                value = keys_login.pop(0)
            form_data1[name] = value
    log.log(f">>> Sending first form to: {form1_url}")
    response1 = presession.post(form1_url, data=form_data1, allow_redirects=True)
    parsed_url = urlparse(response1.url)
    ksnplsid = parse_qs(parsed_url.query).get("KSNPLSID", [None])[0]
    log.log(response1.text)
    log.log(f">>> Response URL: {response1.url}")

    if not ksnplsid:
        log.log("❌ KSNPLSID nem található az URL-ben!")
        log.save()
        raise Exception("KSNPLSID nem található az URL-ben!")
    
    soup = BeautifulSoup(response1.text, 'html.parser')
    status = soup.find('div', id='hideMe').text.strip()

    log.log(f">>> Status: {status}")

    if not status.startswith("OK"):
        log.log("❌ Login failed!")
        log.save()
        raise Exception("Login failed! status: "+ status)
    
    log.log(f">>> KSNPLSID: {ksnplsid}")

    log.log(">>> Login successful!")
    return ksnplsid, log

    

    
#test




    
