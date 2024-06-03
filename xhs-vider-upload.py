import asyncio
import json
import os
import random
from playwright.async_api import Playwright, async_playwright, expect
from dotenv import load_dotenv
load_dotenv()

async def init_browser(playwright): 
    print('init browser')
    browser = await playwright.chromium.launch_persistent_context(# 打开浏览器
    user_data_dir=None,# 浏览器数据保存路径
    executable_path=os.getenv('CHROME_BIN'),# 指定浏览器路径
    accept_downloads=True,# 接受下载
    headless=False,# 无头模式
    bypass_csp=True,# 绕过CSP
    slow_mo=10,# 慢速模式
    args=['--disable-blink-features=AutomationControlled'] #跳过检测
    )
    browser.set_default_timeout(60*1000)
    return browser

async def load_cookies(cookie_file, browser):
    print('load cookies')
    with open(cookie_file, 'r') as f:
        cookies = json.load(f)
        await browser.add_cookies(cookies)
       
async def save_cookies(cookie_file, page):
    print('save cookies')
    cookies = await page.context.cookies()
    with open(cookie_file, 'w') as f:
        json.dump(cookies, f)

def get_cover(folder_path):
    # 列出文件夹下所有的文件名
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    # 筛选出图片文件，这里以.jpg和.png为例
    images = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    # 随机选择一张图片
    random_image = random.choice(images) if images else None
    # 返回图片的完整路径
    return os.path.join(folder_path, random_image) if random_image else None

async def xhs(browser):
    
    cookies = os.getenv('COOKIES_XHS')
    if os.path.exists(cookies):
        await load_cookies(cookies, browser)
        
    page=await browser.new_page()

    url='https://creator.xiaohongshu.com/'
    await page.goto(url)
    await page.wait_for_load_state('load')
    
    is_login2=await page.locator("img").is_visible()
    print("""是否登录创作服务平台:""",is_login2)
    if not is_login2:
        print('未登录创作服务平台, 开始登录')
        try:
            await page.locator('img.css-wemwzq').click()
            await page.wait_for_selector('a.btn')
        except Exception as e:
            print(e)
            return
        
    await page.wait_for_load_state('load')
    print('登录创作服务平台成功')
    await save_cookies(cookies, page)
    
    await page.locator('a.btn').click()
    
    print("视频地址:",video)
    await page.locator('div.drag-over input').set_input_files(video)
    await page.wait_for_selector('div.titleInput input')
    print('上传视频成功')
    
    title= os.getenv('TITLE')
    await page.locator('div.titleInput input').first.fill(title)
    print('填写标题成功')
    
    # 描述
    # description=os.getenv('TITLE')
    description=os.getenv('DESCRIPTION')
    tag=os.getenv('TAGS')
    await page.locator('#post-textarea').fill(description+title+tag)
    print('填写描述成功')
    
    # 发布
    await page.wait_for_timeout(10000)
    await page.get_by_role("button", name="发布").click()
    print('发布成功')
        
    await page.pause()

async def main():
    
    async with async_playwright() as p:
        browser=await init_browser(p)
        await xhs(browser)

if __name__ == '__main__':
    video=os.getenv('VIDEO_PATH')
    asyncio.run(main())