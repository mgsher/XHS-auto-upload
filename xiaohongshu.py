import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import Config
import Cookie
import Init
import Create


def select_user():
    while Config.UserList:
        for i, v in enumerate(Config.UserList):
            print(f"{i + 1}.{v}", end="\t")
        select = input("\nSelect account (Enter 'n' to log in by phone number)：")
        if select == 'n':
            # log in by phone num
            Config.login_status = True
            return
        try:
            Config.CurrentUser = Config.UserList[int(select) - 1]
            return
        except (ValueError, IndexError):
            print("Invalid number")


def login_successful(name_content = None):
    # get ID
    # name_content = WebDriverWait(Config.Browser, 10, 0.2).until(
    #         lambda x: x.find_element(By.XPATH, "//span[@class='channel' and contains(text(), '我')]")).text 

    if name_content is None:
        name_content = WebDriverWait(Config.Browser, 10, 0.2).until(
            lambda x: x.find_element(By.CSS_SELECTOR, ".name-box")).text
    print(f"{name_content}, log in successful")
    #Config.Browser.get("https://creator.xiaohongshu.com/publish/publish")
    Config.Browser.get("https://www.xiaohongshu.com")
    Config.CurrentUser = name_content
    
    Cookie.get_new_cookie()
    Cookie.save_cookie()


def cookie_login():
    Cookie.set_cookie()
    try:
        # WebDriverWait(Config.Browser, 10, 0.2).until(
        #     lambda x: x.find_element(By.CSS_SELECTOR, ".name-box")).text
        
        print(WebDriverWait(Config.Browser, 20, 3).until(
            lambda x: x.find_element(By.XPATH, "//span[@class='channel' and contains(text(), '我')]")).text)
    except TimeoutException:
        Config.login_status = True
        print(TimeoutException)
        return
    login_successful('testing user')


def login():
    #Config.Browser.get("https://www.xiaohongshu.com/")
    Config.Browser.get("https://creator.xiaohongshu.com/login")
    if not Config.login_status:
        cookie_login()
        return
    
    region_selector = Config.Browser.find_element(By.XPATH, "//div[@class='slot-right']")
    region_selector.click()

    # TODO: modify XPATH to more robust, relative path, right now I can only get this to work
    us_selector = WebDriverWait(Config.Browser, 10, 0.2).until(
            lambda x: x.find_element(By.XPATH, "/html/body/div[4]/div/div/div/div[7]/div")
            ) 
    us_selector.click()
    
    while True:
        phone = input("phone number (China Mainland):")
        if len(phone) == 11 or len(phone) == 10:
            break
        print("Invalid phone number")
    
    # send verification

    input_phone = Config.Browser.find_element(By.CSS_SELECTOR,"input[placeholder='手机号']")
    input_phone.send_keys(phone)

    send_code_button = Config.Browser.find_element(By.XPATH, "//*[contains(text(), '发送验证码')]")
    send_code_button.click()

    code = input("Verification code:")
    # back to previous menu
    if code.lower() == 'back':
        return login() 
    
    while len(code) != 6:
        print("Verification code must be 6 digits, please try again")
        code = input("Verification code:")

    code_input = Config.Browser.find_element(By.CSS_SELECTOR, "input[placeholder='验证码']")
    code_input.send_keys(code)

    login_button = Config.Browser.find_element(By.CSS_SELECTOR, "button.css-1jgt0wa.css-kyhkf6")
    login_button.click()

    login_successful()


def login_explore():
    print("get initial browser info")
    Config.Browser.get("https://www.xiaohongshu.com")
    print("clicking initial login button")
    if not Config.login_status:
        cookie_login()
        return
    
    login_button = WebDriverWait(Config.Browser, 10, 0.2).until(
            lambda x: x.find_element(By.ID, "login-btn"))
    print(login_button.get_attribute('class'))
    Config.Browser.execute_script("arguments[0].click();", login_button)
    #login_button.click()
    print("clicked")

    while True:
        phone = input("phone number (China Mainland):")
        if len(phone) == 11:
            break
        print("Invalid phone number")
    
    # send verification
    input_phone = Config.Browser.find_element(By.CSS_SELECTOR,"input[placeholder='输入手机号']")
    input_phone.send_keys(phone)
    print("phone num inputted!")
    send_code_button = WebDriverWait(Config.Browser, 20, 0.2).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@class='code-button active' and contains(text(), '获取验证码')]"))
    )
    #send_code_button = Config.Browser.find_element(By.XPATH, "//span[@class='code-button active' and contains(text(), '获取验证码')]")
    print('veri code')
    print(send_code_button.get_attribute('class'))
    send_code_button.click()

    print("veri code sent!")
    code = input("Verification code:")
    # back to previous menu
    if code.lower() == 'back':
        return login() 
    
    while len(code) != 6:
        print("Verification code must be 6 digits, please try again")
        code = input("Verification code:")

    code_input = Config.Browser.find_element(By.CSS_SELECTOR, "input[placeholder='输入验证码']")
    code_input.send_keys(code)
    print("searching for radio button")
    agreement_radio = Config.Browser.find_element(By.XPATH, "//svg[@class='reds-icon radio']")
    agreement_radio.click()
    print("searching for final login button button")
    login_button = Config.Browser.find_element(By.XPATH, "//button[@class='submit' and contains(text(), '登录')]")
    login_button.click()

    login_successful()


def switch_users():
    print("Logging out...")
    Config.Browser.delete_all_cookies()
    select_user()
    login()


def Quit():
    Cookie.save_cookie()
    print("Script exiting...")
    Config.Browser.quit()
    sys.exit(0)


def select_create():
    while True:
        if Config.Browser.current_url != "https://creator.xiaohongshu.com/publish/publish":
            Config.Browser.get("https://creator.xiaohongshu.com/publish/publish")
        print("1.Video Upload 2.Image Upload 3.Switch User 4.Exit")
        select = input("Select function:")
        match select:
            case '1':
                Create.create_video()
                return
            case '2':
                Create.create_image()
                return
            case '3':
                switch_users()
                return
            case '6':
                Quit()
                return
            case default:
                print("Invalid number")


def start():
    try:
        # initialize
        print("Welcome to the XHS auto-uploading helper, at any time, \n use 'ctrl+c' to exit this script, \n and enter 'back' to go back to the previous menu")
        Init.init()
        select_user()
        
        #login()
        login_explore()
        while True:
            # select function
            select_create()
    except KeyboardInterrupt:
        print("\nExiting...")
    # except Exception as e:
    #     print(f"Error happened：\n{e}")
