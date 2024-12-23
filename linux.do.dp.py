import time
import os
import random
from DrissionPage import Chromium, ChromiumOptions

def load_all_topics(tab):
    """滚动加载话题"""
    scroll_duration = random.uniform(2, 5)
    end_time = time.time() + scroll_duration
    
    print('滚动加载话题')
    try:
        while time.time() < end_time:
            tab.scroll.down(500)
            time.sleep(0.1)
    except Exception as e:
        print(f'滚动加载失败: {e}')

def visit_topics(tab):
    """访问话题"""
    try:
        for i in range(56, 65):
            try:
                topic_element = tab.ele(f'@id=ember{i}')
                if topic_element:
                    topic_id = topic_element.attr('data-topic-id')
                    if topic_id:
                        print(f"[+] 元素 {i} 的 data-topic-id: {topic_id}")
                        
                        tab.get(f"https://linux.do/t/topic/{topic_id}")
                        time.sleep(2)
                        
                        title = tab.ele('@id=topic-title')
                        if title:
                            print(f"[+] 已打开话题: {title.text}")
                        
                        tab.get("https://linux.do/")
                        time.sleep(1)
            except Exception as e:
                print(f"[-] 处理元素 {i} 时出错: {e}")
                continue
    except Exception as e:
        print(f"访问话题失败: {e}")

def logout(tab):
    """退出登录"""
    try:
        tab.ele('@id=toggle-current-user').click()
        time.sleep(1)
        
        tab.ele('@id=user-menu-button-profile').click()
        time.sleep(1)

        tab.ele('css:li.logout button.profile-tab-btn').click()
        time.sleep(2)
        
        tab.refresh()
        login_button = tab.ele('css:.header-buttons .login-button')
        if login_button:
            print("登出成功")
        else:
            print("登出失败")
            
    except Exception as e:
        print(f"登出过程中发生错误: {e}")

account = os.getenv("LINUXDO_USERNAME")
password = os.getenv("LINUXDO_PASSWORD")

co = ChromiumOptions()
co.set_argument('--no-sandbox')
co.set_argument('--headless=new')
co.set_argument('--disable-blink-features=AutomationControlled')
# co.headless()
co.set_user_agent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.3029.110 Safari/537.3')

browser = Chromium(co)
tab = browser.new_tab()
tab.get('https://linux.do')

try:
    tab.ele('登录').click()
    tab.ele('@type=email').input(account)
    tab.ele('@type=password').input(password)
    tab.ele('@id=login-button').click()
    time.sleep(3)

    print(tab.ele('xpath://*[@id="main-outlet"]/div[3]/div[1]').text)
    print(tab.title)

    tab.get('https://connect.linux.do/')
    print(tab.ele('xpath://html/body/h1').text)

    tab.get('https://linux.do/')

    load_all_topics(tab)

    visit_topics(tab)

    logout(tab)

except Exception as e:
    print('登录失败', e)

input('按任意键退出')
browser.quit()
