import json
import os

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from pyvirtualdisplay import Display

from webdriver_manager.chrome import ChromeDriverManager




import Config


def init_browser():
    # display = Display(visible=1, size=(1600, 902))
    # display.start()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--profile-directory=Default')
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-plugins-discovery")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    Config.Browser = webdriver.Chrome(chrome_options = chrome_options)
    Config.Browser.delete_all_cookies()
    Config.Browser.set_window_size(800,800)
    Config.Browser.set_window_position(0,0)
    print('arguments done')


    
    
    # options = Options()
    # options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument('--disable-gpu')
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('--no-sandbox')
    # options.add_argument(f'user-agent={UserAgent().random}')    
    # options.add_argument('--headless')
    # # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # # options.add_experimental_option('useAutomationExtension', False)

    # profile = FirefoxProfile()
    # profile.set_preference('devtools.jsonview.enabled', False)
    # profile.update_preferences()
    # desired = DesiredCapabilities.FIREFOX

    # PROXY = "82.64.77.30:80"

    # proxy = Proxy({
    #             'proxyType': ProxyType.MANUAL,
    #             'httpProxy': PROXY,
    #             'ftpProxy': PROXY,
    #             'sslProxy': PROXY,
    #             #'noProxy': '' # set this value as desired
    #             })
    # proxy.autodetect = False


    #options.add_argument("--proxy-server={}".format('188.166.17.18')) 
    # set proxy
    # PROXY = 
    # firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
    # firefox_capabilities['marionette'] = True
    # firefox_capabilities['proxy'] = {
    #     'proxyType': "MANUAL",
    #     'httpProxy': PROXY,
    #     'ftpProxy': PROXY,
    #     'sslProxy': PROXY
    # }

    # Config.Browser = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver', firefox_profile=profile, options=options, desired_capabilities=desired)
    # Config.Browser.maximize_window()


def init_cookie():
    if os.path.isfile("cookies.json"):
        with open("cookies.json", "r+", encoding="utf-8") as f:
            content = f.read()
            if content:
                Config.CookiesDict.update(json.loads(content))
            else:
                print("Cookie file is empty")
                Config.login_status = True
                return
    else:
        print("Cookie file not exist")
        Config.login_status = True
        return


def init_user():
    for k, _ in Config.CookiesDict.items():
        Config.UserList.append(k)


def init():
    init_cookie()
    init_user()
    init_browser()
