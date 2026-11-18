from playwright.async_api import async_playwright
from utils.logger import logger_init

logger = logger_init()


async def collect_sitemap(url_sitemap: str) -> str:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        try:
            page = await browser.new_page()

            response = await page.goto(
                url_sitemap,
                wait_until="domcontentloaded",
                timeout=30000,
            )

            if not response or response.status != 200:
                error_msg = f"Sitemap request failed: {response.status if response else 'No response'}"
                logger.error(error_msg)
                raise RuntimeError(error_msg)

            xml = await response.text()
            logger.info("Xml collected")
            return xml

        finally:
            await browser.close()
