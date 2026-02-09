import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        # 불필요한 이미지/폰트 로딩 차단 (속도+용량 최적화)
        await page.route("**/*.{png,jpg,jpeg,gif,css,woff}", lambda route: route.abort())
        
        await page.goto("https://www.google.com/search?q=인터넷+사은품+많이주는곳&num=20")
        items = await page.query_selector_all('div.g')
        
        content = "<html><body style='line-height:2; padding:30px;'><h1>🎁 실시간 사은품 TOP 20</h1><hr>"
        for i, item in enumerate(items[:20]):
            t = await item.query_selector('h3')
            l = await item.query_selector('a')
            if t and l:
                content += f"<p>{i+1}. <a href='{await l.get_attribute('href')}'>{await t.inner_text()}</a></p>"
        content += "</body></html>"
        
        with open("index.html", "w", encoding="utf-8") as f: f.write(content)
        await browser.close()

if __name__ == "__main__": asyncio.run(run())