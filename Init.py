"""
Copyright (C) 2023 musicnbrain.org

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import json
import os

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import Config


def init_browser():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument(f'user-agent=={UserAgent().random}')
    
    options.add_argument('--headless')

    Config.Browser = webdriver.Firefox(options=options)
    Config.Browser.maximize_window()


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
        print("Cookie file doesn't exist")
        Config.login_status = True
        return


def init_user():
    for k, _ in Config.CookiesDict.items():
        Config.UserList.append(k)


def init():
    init_cookie()
    init_user()
    init_browser()
