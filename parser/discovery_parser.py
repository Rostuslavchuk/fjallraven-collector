from lxml import etree
from models.models import SitemapURLs
from pydantic import HttpUrl


BLACK_LIST = [
    "/about/",
    "/legal/",
    "/customer-service/",
    "/trouser-guide/",
    "/error-pages/",
    "/my-account/",
    "/checkout/",
    "/nature-is-waiting/",
    "/industry-pro-registration/",
    "/best-sellers/",
    "/explore-",
    "/media-hub/",
    "/resource-center/",
    "/store-locator/",
]


def filter_url(url: HttpUrl) -> bool:
    path = url.path

    is_trash = any(item in path for item in BLACK_LIST)

    url_parts = [
        part for part in path.split("/") if part and part not in ("us", "en-us")
    ]

    is_category = len(url_parts) <= 3

    return not is_trash and not is_category


def parse_sitemap(xml: str) -> SitemapURLs:
    root = etree.fromstring(xml.encode("utf-8"))

    urls = root.xpath("//*[local-name()='url']/*[local-name()='loc']/text()")

    return SitemapURLs(urls=[url for url in map(HttpUrl, urls) if filter_url(url)])
