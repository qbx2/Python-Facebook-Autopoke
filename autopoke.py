email = "" # string
passwd = "" # string
user = 0 # integer

from pycurl import *
import certifi
import StringIO
import BeautifulSoup
import time
import traceback

body = StringIO.StringIO()
curl = Curl()
curl.setopt(COOKIEFILE, "")
curl.setopt(TIMEOUT, 10)

curl.setopt(URL, "https://m.facebook.com/login.php?refsrc=https%3A%2F%2Fm.facebook.com%2F&refid=8")
curl.setopt(CAINFO, certifi.where())
curl.setopt(POSTFIELDS, "lsd=AVr6bag0&charset_test=%E2%82%AC%2C%C2%B4%2C%E2%82%AC%2C%C2%B4%2C%E6%B0%B4%2C%D0%94%2C%D0%84&version=1&ajax=0&width=0&pxr=0&gps=0&m_ts=1392773888&li=AAsEU-_VkZYJT40foTcvOgVj&signup_layout=layout%7Clower_subdued_button%7C%7Cs_btn%7Cspecial%7C%7Cl_btn%7Cconfirm%7C%7Csignupinstr%7C%7Clogininstr%7C%7Cst%7Ccreate%7C%7Claunched_Jan9&email="+email+"&pass="+passwd+"&login=%EB%A1%9C%EA%B7%B8%EC%9D%B8")
curl.perform()

print "Login Complete"

curl.setopt(WRITEFUNCTION, body.write)
curl.setopt(USERAGENT, "Windows NT AppleWebKit Chrome")

while True:
    curl.setopt(URL, "https://m.facebook.com/pokes/")
    curl.setopt(POST, False)
    body.truncate(0)
    try:
        curl.perform()
    except KeyboardInterrupt:
        raise SystemExit
    except:
        time.sleep(10)
        traceback.print_exc() 
        continue

    dtsg = body.getvalue()
    dtsg = dtsg[dtsg.find("token\"")+len("token\"")+2:]
    dtsg = dtsg[:dtsg.find("\"")]
    
    bs = BeautifulSoup.BeautifulSoup(body.getvalue())

    for x in filter(lambda x : x.has_key('data-ajaxify-href') and x['data-ajaxify-href'].find("suggestion_type=") == -1 and x['data-ajaxify-href'].find("is_hide=0") != -1, bs.findAll("a")):
        # "https://m.facebook.com" + x['href']
        curl.setopt(URL, "https://m.facebook.com%s"%str(x['data-ajaxify-href']))
        curl.setopt(POSTFIELDS, "m_sess=&fb_dtsg=" + dtsg + "&__dyn=&__req=m&__ajax__=true&__user=%d"%user)
        body.truncate(0)
        try:
            curl.perform()
        except KeyboardInterrupt:
            raise SystemExit
        except:
            time.sleep(10)
            continue

        while "You have poked users too many times recently" in body.getvalue():
            print time.strftime("[%Y-%m-%d %H:%M:%S] Failed To Poke Back!")
            time.sleep(90)
            try:
                body.truncate(0)
                curl.perform()
            except KeyboardInterrupt:
                raise SystemExit
            except:
                time.sleep(10)

        try:
            name = x.parent.parent.parent.parent.find("i").parent['href'][1:]
            print time.strftime("[%Y-%m-%d %H:%M:%S] ") + "Poked %s Back!"%name
        except:
            traceback.print_exc()

        time.sleep(1)

    #print "Sleep(10)"
