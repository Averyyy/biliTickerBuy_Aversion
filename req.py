# 本文件已弃用
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# 加载配置文件
with open('./config.json', 'r') as f:
    config = json.load(f)

url = "https://show.bilibili.com/platform/confirmOrder.html?token=wGRNCQ4AARqAAAHu6wEAAQAF0Ag.&project_id=72320"

# 创建WebDriver实例
driver = webdriver.Chrome()

# 如果没有提供Cookie，手动登录
if len(config["bilibili_cookies"]) == 0:
    driver.get("https://passport.bilibili.com/login")
    print("请登录")
    
    while True:
        try:
            driver.find_element(By.CLASS_NAME, "nav-user-center")
            break
        except:
            time.sleep(1)

    config["bilibili_cookies"] = driver.get_cookies()
    with open('./config.json', 'w') as f:
        json.dump(config, f, indent=4)

# 使用Cookie登录
driver.get(url)
for cookie in config["bilibili_cookies"]:
    my_cookie = {
        'domain': cookie['domain'],
        'name': cookie['name'],
        'value': cookie['value'],
        'path': cookie['path'],
    }
    if 'expiry' in cookie:
        my_cookie['expiry'] = cookie['expiry']
    if 'httpOnly' in cookie:
        my_cookie['httpOnly'] = cookie['httpOnly']
    if 'sameSite' in cookie:
        my_cookie['sameSite'] = cookie['sameSite']
    if 'secure' in cookie:
        my_cookie['secure'] = cookie['secure']

    driver.add_cookie(my_cookie)
driver.get(url)

# 等待页面加载
wait = WebDriverWait(driver, 5)

while True:
    try:
        # 等待确认按钮出现并可点击
        confirm_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".confirm-paybtn.active")))

        # 持续点击确认按钮
        while True:
            confirm_button.click()
            print("点击确认按钮")
            time.sleep(1)

    except TimeoutException:
        # 如果未找到按钮或按钮不可点击，刷新页面并重试
        print("刷新页面")
        driver.refresh()

# 关闭WebDriver实例
driver.quit()
