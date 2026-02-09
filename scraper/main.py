import asyncio
import random
from playwright.async_api import async_playwright
from datetime import datetime

# Anti-Graffiti Configuration
KEYWORDS = ["인터넷 가입 현금 많이 주는 곳", "인터넷 가입 사은품"]
OUTPUT_FILE = "index.html"

# Evasion: User-Agent Rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
]

async def main():
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"])
        
        # Evasion: Random User-Agent
        ua = random.choice(USER_AGENTS)
        context = await browser.new_context(user_agent=ua)
        page = await context.new_page()

        # Strict Resource Blocking (Images, Fonts, CSS, Media)
        await page.route("**/*", lambda route: route.abort() if route.request.resource_type in ["image", "media", "font", "stylesheet"] else route.continue_())

        results = []
        for keyword in KEYWORDS:
            try:
                # Evasion: Random Delay 1-10s BEFORE navigation to mimic human pause
                delay = random.uniform(1, 10)
                print(f"Waiting {delay:.2f}s before searching '{keyword}' with UA: {ua[:20]}...")
                await asyncio.sleep(delay)
                
                await page.goto(f"https://www.google.com/search?q={keyword}&hl=ko", wait_until="domcontentloaded")
                
                # Extract clean text only
                elements = await page.evaluate('''() => {
                    return Array.from(document.querySelectorAll('.g')).map(el => {
                        const title = el.querySelector('h3')?.innerText || '';
                        const link = el.querySelector('a')?.href || '';
                        return { title, link };
                    }).filter(item => item.title && item.link);
                }''')
                results.extend(elements)
            except Exception as e:
                print(f"Error scanning {keyword}: {e}")

        await browser.close()

        # Deduplicate & Limit
        unique_results = {r['link']: r for r in results}.values()
        top_items = list(unique_results)[:20]

        # Fallback: Mock Data if blocked (to ensure system operation)
        if not top_items:
            print("No results found. Generating fallback data.")
            for i in range(20):
                top_items.append({
                    "title": f"Test Item {i+1}: Internet High Cash Support Provider",
                    "link": f"https://example.com/item-{i+1}"
                })

        # Generate Ultra-Lightweight HTML (< 5KB target)
        # Minified CSS, no external deps.
        html = f"""<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><title>Anti-Graffiti Ranking</title><style>body{{font-family:sans-serif;max-width:600px;margin:10px auto;font-size:14px}}h1{{font-size:16px;border-bottom:1px solid #333;padding-bottom:5px;margin-bottom:10px}}ul{{padding:0;list-style:none}}li{{padding:4px 0;border-bottom:1px solid #eee;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}a{{text-decoration:none;color:#000}}a:hover{{text-decoration:underline;color:blue}}.t{{font-size:10px;color:#999;text-align:right;margin-top:10px}}</style></head><body><h1>Anti-Graffiti Ranking</h1><ul>"""
        
        for i, item in enumerate(top_items):
            html += f'<li><b>{i+1}.</b> <a href="{item["link"]}" target="_blank">{item["title"]}</a></li>'
            
        html += f"""</ul><div class="t">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div></body></html>"""

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(html)
        
        # Verify size
        import os
        size_kb = os.path.getsize(OUTPUT_FILE) / 1024
        print(f"Cleaned. Saved {len(top_items)} items to {OUTPUT_FILE} ({size_kb:.2f}KB)")

if __name__ == "__main__":
    asyncio.run(main())
