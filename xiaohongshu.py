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
        select = input("\n请选择用户(输入'n'使用手机号登录)：")
        if select == 'n':
            # 手机号登录
            Config.login_status = True
            return
        try:
            Config.CurrentUser = Config.UserList[int(select) - 1]
            return
        except (ValueError, IndexError):
            print("请输入有效的手机号")


def login_successful():
    # 获取昵称
    name_content = WebDriverWait(Config.Browser, 10, 0.2).until(
        lambda x: x.find_element(By.CSS_SELECTOR, ".name-box")).text
    print(f"{name_content},登录成功!")
    Config.Browser.get("https://creator.xiaohongshu.com/publish/publish")
    Config.CurrentUser = name_content
    # 获取Cookie
    Cookie.get_new_cookie()
    Cookie.save_cookie()


def cookie_login():
    Cookie.set_cookie()
    try:
        WebDriverWait(Config.Browser, 10, 0.2).until(
            lambda x: x.find_element(By.CSS_SELECTOR, ".name-box")).text
    except TimeoutException:
        Config.login_status = True
        return
    login_successful()


def login():
    Config.Browser.get("https://creator.xiaohongshu.com/login")
    if not Config.login_status:
        cookie_login()
        return
    # 访问登陆页面
    while True:
        phone = input("请输入手机号：")
        if len(phone) == 11:
            break
        print("手机号码不合法！")
    input_phone = Config.Browser.find_element(By.CSS_SELECTOR,"input[placeholder='手机号']")
    input_phone.send_keys(phone)

    # 等待验证码链接可点击
    send_code_button = Config.Browser.find_element(By.XPATH, "//*[contains(text(), '发送验证码')]")
    send_code_button.click()

    # 等待用户输入验证码
    code = input("请输入验证码：")
    while len(code) != 6:
        print("验证码长度必须是6位！")
        code = input("请重新输入验证码：")

    # 找到验证码输入框并输入验证码
    code_input = Config.Browser.find_element(By.CSS_SELECTOR, "input[placeholder='验证码']")
    code_input.send_keys(code)

    # 找到登录按钮并点击
    login_button = Config.Browser.find_element(By.CSS_SELECTOR, "button.css-1jgt0wa.css-kyhkf6")
    login_button.click()

    # 登录
    #login_btn = 'return document.querySelector("#page > div > div.content > div.con > div.login-box-container > div > ' \
    #            'div > div > div > div:nth-child(2) > button")'
    #Config.Browser.execute_script(login_btn).click()
    login_successful()


def switch_users():
    print("正在清除Cookie")
    Config.Browser.delete_all_cookies()
    select_user()
    login()


def Quit():
    Cookie.save_cookie()
    print("正在退出...")
    Config.Browser.quit()
    sys.exit(0)


def select_create():
    while True:
        if Config.Browser.current_url != "https://creator.xiaohongshu.com/publish/publish":
            Config.Browser.get("https://creator.xiaohongshu.com/publish/publish")
        print("1. 视频上传  2.图文上传  3. 切换用户 4.退出")
        select = input("请选择功能：")
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
            case '4':
                Quit()
                return
            case default:
                print("请输入有效的数字")


def start():
    try:
        # 初始化程序
        print("正在初始化程序...")
        Init.init()
        # 选择用户
        select_user()
        # 登录
        login()
        while True:
            # 选择功能
            select_create()
    except KeyboardInterrupt:
        print("\n正在退出...")
    except Exception as e:
        print(f"发生了一些错误：\n{e}")
