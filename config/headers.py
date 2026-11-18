from urllib.parse import urlparse

PDP_HEADERS = {
    "accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,"
        "image/jxl,image/avif,image/webp,image/apng,*/*;q=0.8,"
        "application/signed-exchange;v=b3;q=0.7"
    ),
    "accept-language": "en",
    "cache-control": "max-age=0",
    "priority": "u=0, i",
    "sec-ch-ua": ('"Not:A-Brand";v="8", "Chromium";v="156", "Google Chrome";v="156"'),
    "sec-ch-ua-arch": '"arm"',
    "sec-ch-ua-bitness": '"64"',
    "sec-ch-ua-full-version": '"156.0.8078.48"',
    "sec-ch-ua-full-version-list": (
        '"Not:A-Brand";v="8.0.0.0", '
        '"Chromium";v="156.0.8078.48", '
        '"Google Chrome";v="156.0.8078.48"'
    ),
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": '""',
    "sec-ch-ua-platform": '"macOS"',
    "sec-ch-ua-platform-version": '"27.2.0"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "cross-site",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/156.0.0.0 Safari/537.36"
    ),
}


def reviews_headers(cookies, main_url):
    parsed = urlparse(main_url)
    origin = f"{parsed.scheme}://{parsed.netloc}"

    return {
        "cookie": "; ".join(
            [f"{key}={name}" for key, name in cookies.get_dict().items()]
        ),
        "referer": origin + "/",
        "origin": origin,
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
        "accept": "application/json",
        "bv-bfd-token": "27893,main_site,en_US",
    }


def reviews_config():
    return {
        "api": "https://apps.bazaarvoice.com/bfd/v1/clients/fenix_outdoor/api-products/cv2/resources/data/reviews.json",
        "params": lambda product_id: {
            "resource": "reviews",
            "action": "REVIEWS_N_STATS",
            "filter": [
                f"productid:eq:{product_id}",
                "contentlocale:eq:da*,nl*,en*,fi*,fr*,de*,it*,no*,sv*,en_US,en_US",
                "isratingsonly:eq:false",
            ],
            "filter_reviews": "contentlocale:eq:da*,nl*,en*,fi*,fr*,de*,it*,no*,sv*,en_US,en_US",
            "include": "authors,products,comments",
            "filteredstats": "reviews",
            "Stats": "Reviews",
            "limit": 15,
            "offset": 0,
            "sort": "ContentLocale:en_US",
            "apiversion": 5.5,
            "displaycode": "27893-en_us",
        },
    }
