import asyncio
import json
import traceback
from concurrent.futures import ProcessPoolExecutor

from models.models import PDPModel
from utils.logger import logger_init
from storage.scheduler import SchedulerStorage
from parser.pdp_parser import parse_pdp, parse_window_field

from fetcher.pdp_collection import FetcherActions

logger = logger_init()


def parse_pdp_process(
    html, json_reviews_str, window_data_str, pdp_url
) -> PDPModel | None:
    json_reviews = (
        json.loads(json_reviews_str)
        if isinstance(json_reviews_str, str)
        else json_reviews_str
    )
    window_data = (
        json.loads(window_data_str)
        if isinstance(window_data_str, str)
        else window_data_str
    )

    return parse_pdp(html, json_reviews, window_data, pdp_url)


async def worker(queue, pool, fetcher):
    loop = asyncio.get_running_loop()

    while True:
        pdp_url = await queue.get()

        try:
            if pdp_url is None:
                return

            html_page = await fetcher.pdp_collect(pdp_url)
            if html_page is None:
                logger.warning(f"Html page is not collected: {pdp_url}")
                continue

            window_data = await asyncio.to_thread(parse_window_field, html_page)

            code = window_data.get("code") if window_data else None
            if not code:
                logger.warning(f"Missing product code: {pdp_url}")
                SchedulerStorage().set_category_pdp_storage(pdp_url)
                continue

            json_reviews = await fetcher.reviews_collect(code, pdp_url)

            result = await loop.run_in_executor(
                pool,
                parse_pdp_process,
                html_page,
                json.dumps(json_reviews),
                json.dumps(window_data),
                pdp_url,
            )

            if result:
                SchedulerStorage().set_pdp_storage(result.model_dump(mode="json"))

        except Exception:
            logger.exception(f"Worker error: {pdp_url}")
            traceback.print_exc()

        finally:
            queue.task_done()


async def main():
    json_urls = await asyncio.to_thread(SchedulerStorage().get_sitemap_storage)

    async with FetcherActions() as fetcher:
        queue = asyncio.Queue()

        for pdp_url in json_urls:
            await queue.put(pdp_url)

        with ProcessPoolExecutor(max_workers=2) as pool:
            workers = [
                asyncio.create_task(worker(queue, pool, fetcher)) for _ in range(5)
            ]

            await queue.join()

            for _ in workers:
                await queue.put(None)

            await asyncio.gather(*workers)


if __name__ == "__main__":
    asyncio.run(main())
