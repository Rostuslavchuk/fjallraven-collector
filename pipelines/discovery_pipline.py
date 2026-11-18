import traceback
import asyncio
import argparse
from concurrent.futures import ProcessPoolExecutor

from fetcher.discovery_collection import collect_sitemap
from models.models import SitemapURLs
from parser.discovery_parser import parse_sitemap

from storage.scheduler import SchedulerStorage
from utils.logger import logger_init


logger = logger_init()


def parse_sitemap_process(xml: str) -> SitemapURLs:
    return parse_sitemap(xml)


async def worker(queue, pool):
    loop = asyncio.get_running_loop()

    while True:
        data = await queue.get()

        try:
            if data is None:
                return

            xml = await collect_sitemap(data)

            result = await loop.run_in_executor(pool, parse_sitemap_process, xml)
            urls = result.model_dump(mode="json")
            logger.info("Pdps parsed")
            SchedulerStorage().set_sitemap_storage(data=urls)
            logger.info("Pdps saved to storage")

        except Exception as e:
            logger.exception("Worker failed")
            traceback.print_exc()

        finally:
            queue.task_done()


async def main():
    parser = argparse.ArgumentParser(description="Sitemap url")
    parser.add_argument(
        "-u",
        "--url",
        type=str,
        required=True,
        help="URL to process",
    )
    args = parser.parse_args()

    queue = asyncio.Queue()
    await queue.put(args.url)

    with ProcessPoolExecutor(max_workers=1) as pool:
        task = asyncio.create_task(worker(queue, pool))

        await queue.join()

        await queue.put(None)
        await task


if __name__ == "__main__":
    asyncio.run(main())
