import requests
from bs4 import BeautifulSoup
import re

class Suteme:
    def __init__(self, csrf_token=None, sessionhash=None):
        self.csrf_token = csrf_token
        self.sessionhash = sessionhash
        self.session = requests.Session()
        if csrf_token is None and sessionhash is None:
            self.session.post("https://m.kuku.lu/")
            self.csrf_token = self.session.cookies.get("cookie_csrf_token")
            self.sessionhash = self.session.cookies.get("cookie_sessionhash")
        else:
            self.session.cookies.set("cookie_csrf_token",csrf_token)
            self.session.cookies.set("cookie_sessionhash",sessionhash)
            self.session.post("https://m.kuku.lu/")
    
    def check_token(self):
        return self.csrf_token, self.sessionhash
    
    def add_mail(self):
        return self.session.get("https://m.kuku.lu/index.php?action=addMailAddrByAuto&nopost=1&by_system=1").text[3:]
    
    def add_onetime_mail(self):
        onetime_mail = self.session.get("https://m.kuku.lu/index.php?action=addMailAddrByOnetime&nopost=1&by_system=1").text[3:]
        return onetime_mail.split(",")[0]
    
    def get_all_mail(self):
        return self.session.get("https://m.kuku.lu/datagen.php?action=getAddrList").text
    
    def get_top_mail(self, mail):
        mail = mail.replace("@", "%40")
        check_come_mail = self.session.get(f"https://m.kuku.lu/recv._ajax.php?&q={mail}&&nopost=1&csrf_token_check={self.csrf_token}")
        soup = BeautifulSoup(check_come_mail.text, 'html.parser')
        soup = soup.find_all('script')
        soup_text = "".join([str(s) for s in soup])
        match = re.search(r"openMailData\('([^']*)', '([^']*)'", soup_text)
        if match:
            num = match.group(1)
            key = match.group(2)
        else:
            print("メールが来てません。")
            return None, None
        view_mail = self.session.post("https://m.kuku.lu/smphone.app.recv.view.php", data={"num":num, "key":key})
        soup = BeautifulSoup(view_mail.text, "html.parser")
        title = soup.find(class_="full").get_text(strip=True)
        content = soup.find("div", style="height:fit-content;").get_text(strip=True)
        
        return title, content
