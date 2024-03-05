import os.path
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import Config
import Cookie
import Init
import Create


if __name__ == '__main__':
    


    Init.init()
    print("get initial browser info")
    Config.Browser.get("https://www.xiaohongshu.com/explore")

    Config.CurrentUser = 'testing_user'
    
    Cookie.get_new_cookie()
    Cookie.save_cookie()
    # print("input search")
    # search_input = Config.Browser.find_element(By.ID, "search-input")
    # search_content = 946543744
    # search_input.send_keys(search_content)
    # print('clicking')
    # search_button = Config.Browser.find_element(By.XPATH, "//div[@class='search-icon']")
    # search_button.click()

    # Config.Browser.get("https://www.xiaohongshu.com/explore")
    # print("clicking initial login button")
    # login_button = Config.Browser.find_element(By.ID, "login-btn")
    # print(login_button.get_attribute('class'))
    # login_button.click()

    # while True:
    #     print("inputting phone")
    #     phone = input("phone number (China Mainland):")
    #     if len(phone) == 11:
    #         break
    #     print("Invalid phone number")
    
    # # send verification
    # input_phone = Config.Browser.find_element(By.CSS_SELECTOR,"input[placeholder='输入手机号']")
    # input_phone.send_keys(phone)

    # send_code_button = WebDriverWait(Config.Browser, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '获取验证码')]"))
    # )
    # send_code_button.click()

    # code = input("Verification code:")
    # # # back to previous menu
    # # if code.lower() == 'back':
    # #     return login() 
    
    # while len(code) != 6:
    #     print("Verification code must be 6 digits, please try again")
    #     code = input("Verification code:")

    # code_input = Config.Browser.find_element(By.CSS_SELECTOR, "input[placeholder='输入验证码']")
    # code_input.send_keys(code)

    # agreement_radio = Config.Browser.find_element(By.XPATH, "//svg[@class='reds-icon radio']")
    # agreement_radio.click()

    # login_button = Config.Browser.find_element(By.XPATH, "//button[@class='submit' and contains(text(), '登录')]")
    # login_button.click()

    # login_successful()