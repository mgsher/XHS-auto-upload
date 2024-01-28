import os.path
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import Config


def create(create_js):
    print("Uploading...")
    time.sleep(10)
    create_js = f'return document.querySelector("{create_js}")'
    Config.Browser.execute_script(create_js).click()
    print("Published successful")
    print("Going back to the previous menu...")
    time.sleep(5)


def input_title():
    title = input("Enter your title:")
    if title.lower() == 'back':
        return None
    return title


def input_content():
    content_file = input("Enter the path of the content (must be txt):")
    if content_file.lower() == 'back':
        return None
    try:
        with open(content_file, 'r', encoding='utf-8') as file:
            content = file.read().strip()
    except FileNotFoundError:
        print("Path doesn't exist, please try again")
        return input_content()
    return content
    

def input_video_path():
    path_mp4 = input("Enter the path of the video:")
    if path_mp4.lower() == 'back':
        return None
    if not os.path.isfile(path_mp4):
        print("Path doesn't exist, please try again")
        return input_video_path()
    return path_mp4


def input_cover_path():
    path_cover = input("Enter the path of the cover (use the first frame of video by default):")
    if path_cover.lower() == 'back':
        return None
    if path_cover and not os.path.isfile(path_cover):
        print("Path doesn't exist, please try again")
        return input_cover_path()
    return path_cover


def create_video():
    step = "input_video_path"  
    path_mp4 = None
    path_cover = None
    title = None
    content = None

    while True:
        if step == "input_video_path":
            path_mp4 = input_video_path()
            if path_mp4 is None:
                return  
            step = "input_cover_path"  

        elif step == "input_cover_path":
            path_cover = input_cover_path()
            if path_cover is None:
                step = "input_video_path"  
                continue
            step = "input_title"  

        elif step == "input_title":
            title = input_title()
            if title is None:
                step = "input_cover_path"  
                continue
            step = "input_content" 

        elif step == "input_content":
            content = input_content()
            if content is None:
                step = "input_title"  
                continue
            break
    
    # Find the place to upload video
    try:
        WebDriverWait(Config.Browser, 10, 0.2).until(
            lambda x: x.find_element(By.CSS_SELECTOR, "div.tab:nth-child(1)")).click()
    except TimeoutException:
        print("Failed to load the website")

    # Video upload
    Config.Browser.find_element(By.CSS_SELECTOR, ".upload-input").send_keys(path_mp4)
    time.sleep(10)
    print("Video uploading...")
    
    # Wait until completion
    WebDriverWait(Config.Browser, 20).until(
        EC.presence_of_element_located((By.XPATH, r'//*[contains(text(),"重新上传")]'))
    )
    while True:
        time.sleep(3)
        try:
            Config.Browser.find_element(By.XPATH, r'//*[contains(text(),"重新上传")]')
            break
        except Exception:
            print("Video uploading...")

    # Cover upload
    if path_cover != "":
        edit_button = Config.Browser.find_element(By.CSS_SELECTOR, "button.css-k3hpu2.css-osq2ks.dyn.btn.edit-button.red")
        edit_button.click()

        Config.Browser.find_element(By.XPATH, r'//*[text()="上传封面"]').click()
        
        Config.Browser.find_element(By.CSS_SELECTOR, "div.upload-wrapper:nth-child(2) > input:nth-child(1)").send_keys(
            path_cover)

        # Submit cover
        WebDriverWait(Config.Browser, 10, 0.2).until(
            lambda x: x.find_element(By.CSS_SELECTOR, ".css-8mz9r9 > div:nth-child(1) > button:nth-child(2)")).click()
    
    title_input = Config.Browser.find_element(By.CSS_SELECTOR, ".c-input_inner")
    content_input = Config.Browser.find_element(By.CSS_SELECTOR, "#post-textarea")

    title_input.clear()
    title_input.send_keys(title)
    content_input.clear()
    content_input.send_keys(content)
    
    create(".publishBtn")


def input_image_path():
    while True:
        user_input = input("Enter the path of images, use ',' to split multiple:")
        if user_input.lower() == 'back':
            return None
        path_image = user_input.split(',')
        if 0 < len(path_image) <= 9:
            for i in path_image:
                if not os.path.isfile(i):
                    print("Path doesn't exist, please try again")
                    break
            else:
                return "\n".join(path_image)
        elif len(path_image) <= 0:
            print("At least 1 image should be uploaded")
            continue
        else:
            print("At most 9 images should be uploaded")
            continue


def create_image():
    step = "input_image_path"  
    path_image = []
    title = None
    content = None

    while True:
        if step == "input_image_path":
            path_image = input_image_path()
            if path_image is None:  
                return  
            step = "input_title"  

        elif step == "input_title":
            title = input_title()
            if title is None:
                step = "input_image_path"  
                continue
            step = "input_content"  

        elif step == "input_content":
            content = input_content()
            if content is None:
                step = "input_title"  
                continue
            break  
    try:
        WebDriverWait(Config.Browser, 10, 0.2).until(
            lambda x: x.find_element(By.CSS_SELECTOR, "div.tab:nth-child(2)")).click()
    except TimeoutException:
        print("Failed to load the website")
    
    # Image upload
    Config.Browser.find_element(By.CSS_SELECTOR, ".upload-wrapper > div:nth-child(1) > input:nth-child(1)").send_keys(
        path_image)
    print("Image(s) uploading...")
    time.sleep(10)
    title_input = Config.Browser.find_element(By.CSS_SELECTOR, ".c-input_inner")
    content_input = Config.Browser.find_element(By.CSS_SELECTOR, "#post-textarea")

    title_input.clear()
    title_input.send_keys(title)
    content_input.clear()
    content_input.send_keys(content)

    create("button.css-k3hpu2:nth-child(1)")
