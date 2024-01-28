import json
import Config


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
