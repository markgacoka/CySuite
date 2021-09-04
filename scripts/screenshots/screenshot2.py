# Doesn't work but promising... Browser closes unexpectedly
import asyncio
from pyppeteer import launch
from webdriver_manager.chrome import ChromeDriverManager

async def main():
    browser = await launch(executablePath=ChromeDriverManager().install())
    page = await browser.newPage()
    await page.goto('https://example.com')
    await page.screenshot({'path': 'example.png'})
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())