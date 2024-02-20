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
import Config
import time


def set_cookie():
    try:
        for cookie in json.loads(Config.CookiesDict[Config.CurrentUser]):
            Config.Browser.add_cookie(cookie)
        Config.Browser.refresh()
    except KeyError:
        return


def get_new_cookie():
    cookies = json.dumps(Config.Browser.get_cookies())
    Config.CookiesDict[Config.CurrentUser] = cookies


def save_cookie():
    print("Saving Cookie...")
    with open('cookies.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(Config.CookiesDict))
    print('Cookies saved')


def check_cookie_expiry():
    with open('cookies.json', 'r', encoding='utf-8') as f:
        cookies = json.load(f)
        
        current_timestamp = time.time()
        for user_id, user_cookies_str in cookies.items():
            user_cookies = json.loads(user_cookies_str)
            
            # find all expiry timestamps of cookies and make them a list
            expiry_timestamps = [cookie['expiry'] for cookie in user_cookies if 'expiry' in cookie]

            # check if the login session has been expired
            if expiry_timestamps:
                earliest_expiry = min(expiry_timestamps)
                if earliest_expiry < current_timestamp:
                    print(f"User {user_id}'s cookie has been expired, please log in by phone again")
                else:
                    print(f"User {user_id}'s cookie is still valid, logging you in...")
                    return True
            else:
                print(f"No enough info about User {user_id}'s cookie")
    return False