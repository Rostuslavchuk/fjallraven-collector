from curl_cffi.requests import AsyncSession
from playwright.async_api import async_playwright

from models.models import ReviewModel
from utils.logger import logger_init
from config.headers import reviews_headers, reviews_config


logger = logger_init()


class FetcherActions:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.session = None

    async def __aenter__(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        self.context = await self.browser.new_context()
        self.session = AsyncSession(impersonate="chrome124")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    async def pdp_collect(self, pdp_url: str) -> str | None:
        page = await self.context.new_page()

        try:
            response = await page.goto(
                pdp_url, wait_until="domcontentloaded", timeout=30000
            )

            if not response or response.status != 200:
                logger.error(
                    f"Request failed: {pdp_url}, {response.status if response.status else response.body}"
                )
                return None

            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

            return await page.content()

        except Exception as e:
            logger.error(f"Error playwright: {e}")
            return None

        finally:
            await page.close()

    async def reviews_collect(
        self, code: str, pdp_url: str
    ) -> list[ReviewModel] | None:
        try:
            config = reviews_config()
            reviews_api = config["api"]
            reviews_params = config["params"]

            response = await self.session.get(
                url=reviews_api,
                headers=reviews_headers(self.session.cookies, pdp_url),
                params=reviews_params(code),
                timeout=10,
            )

            if response.status_code == 200:
                logger.info(f"Reviews received! Status: {response.status_code}.")
                return response.json()

            logger.error(
                "PDP API response:\n"
                f"Status: {response.status_code}\n"
                f"URL: {response.url}\n"
            )
            return None

        except Exception as e:
            logger.error(f"Error: {e}.")
            return None
