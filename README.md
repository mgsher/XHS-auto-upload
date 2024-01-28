# Xiaohongshu Auto-uploading Helper

## Setup

> Prerequisite:  
> - Python 3.11.1  
> - Download WebDriver provided by Firefox
>   - [geckodriver](https://github.com/mozilla/geckodriver)

### Clone project

```shell
git clone https://github.com/LuckyTime1025/xiaohongshu.git
```

### Enter folder

```shell
cd xiaohongshu
```

### Create virtual environment

```shell
python -m venv venv
```

### Activate virtual environment

```shell
.\venv\Scripts\activate
```

### Install Pypi Dependency

```shell
pip install -r requirements.txt 
```

## Instruction

### Run script

```shell
python main.py
```

### Log in
> Once the script runs, it will first check if ```Cookie``` in ```cookies.json``` is valid. If ```Cookie``` is invalid or the file doesn't exist, user have to use their phone number to receive verification code to log in. Otherwise, the script will log user in through ```Cookie``` by default.
> ```Cookie``` will be saved in ```cookies.json``` once the account is logged in successfully.

### General feature
While using the script, at any time:
> Use 'ctrl + c' to exit the script. 
> Enter 'back' to go back to upper menu.

### Video upload

It's not necessary to upload cover when uploading video. XHS automatically generates cover by using the first frame of the uploaded video. However, user is encouraged to upload more attractive cover manually.

User is allowed to upload image in ```.mp4```, ```.mov```, ```.flv```, ```.f4v```, ```.mkv```, ```.rm```, ```.rmvb```, ```.m4v```, ```.mpg```, ```.mpeg```, and ```.ts``` format.

### Image upload

User should upload at least 1 image and at most 9 images. If user wants to upload multiple images, use ',' (without blankspace!) to split different filepaths of images. 

User is allowed to upload image in ```.jpg```, ```.jpeg```, ```.png```, and ```.webp``` format.

### Content upload (for both video and image cases)

User can enter the title directly while publishing.
As for the content, user should provide a valid filepath of the txt file of the content. User can therefore edit the content in a more flexible way.