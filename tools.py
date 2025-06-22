import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
import random
import time
import os


def update_name(sid, log, username):
    ksnplsid = sid
    username_to_set = username

    mainurl = "https://kisnaplo.karinthy.hu/app/interface.php?view=v_k78_main&KSNPLSID=" + ksnplsid

    session = requests.Session()

    delete_url = f"https://kisnaplo.karinthy.hu/app/interface.php?action=a_k78_logindelete&KSNPLSID={ksnplsid}"
    log.log(">>> Sending GET to logindelete:"+ delete_url)

    session.get(delete_url)

    # 7. Most újra betöltjük a lapot, ahol a 2. form van
    response1 = session.get(mainurl, allow_redirects=True)
    soup2 = BeautifulSoup(response1.text, "html.parser")
    form2 = soup2.find("form", {"name": "k78_logincheck"})
    if not form2:
        raise Exception("Második form nem található")

    action2 = form2.get("action")
    form2_url = urljoin(response1.url, action2)
    inputs2 = form2.find_all("input")
    form_data2 = {}

    # 8. Kitöltjük a második form mezőit
    for tag in inputs2:
        name = tag.get("name")
        value = tag.get("value", "")
        if name == "logincheck":
            value = username_to_set
        form_data2[name] = value

    # 9. Második form elküldése
    log.log(">>> Sending second form to:"+ form2_url)
    response2 = session.post(form2_url, data=form_data2, allow_redirects=True)

    # 10. Eredmény kiírása
    log.log(">>> Final URL after login check:"+ response2.url)
    log.log(">>> Status Code:"+ str(response2.status_code))

def upload_picture(sid, log, pic_path):

    mainurl = "https://kisnaplo.karinthy.hu/app/interface.php?view=v_k78_main&KSNPLSID=" + sid
    session = requests.Session()

    delete_url = f"https://kisnaplo.karinthy.hu/app/interface.php?action=a_k78st5_imagedelete&KSNPLSID={sid}"
    log.log(">>> Sending GET to imagedelete:"+ delete_url)

    session.get(delete_url)

    # 7. Most újra betöltjük a lapot, ahol a 2. form van
    response1 = session.get(mainurl, allow_redirects=True)
    soup = BeautifulSoup(response1.text, "html.parser")

    form = soup.find('form', attrs={'name': 'frm_upload'})
    if not form:
        raise Exception("Form with name='frm_upload' not found.")

    # Extract form details
    action = form.get('action')
    method = form.get('method', 'get').lower()
    enctype = form.get('enctype', 'application/x-www-form-urlencoded')
    
    post_url = "https://kisnaplo.karinthy.hu/app/" + action

    data = {}
    files = {}
    for input_tag in form.find_all('input'):
        name = input_tag.get('name')
        if not name:
            continue
        input_type = input_tag.get('type', 'text')
        value = input_tag.get('value', '')
        if input_type == 'file':
            files[name] = open(pic_path, 'rb') 
        else:
            data[name] = value

    res = session.post(post_url, data=data, files=files)
    
    log.log(">>> Final URL after upload:"+ res.url)
    log.log(">>> Status Code:"+ str(res.status_code))



tools = [
    update_name,
    upload_picture
]
