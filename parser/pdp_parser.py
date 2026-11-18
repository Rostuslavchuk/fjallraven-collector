from lxml import html
import chompjs
import json
import re
from urllib.parse import urljoin

from models.models import PDPModel


def breadcrumbs_url(item: str, pdp_url: str):
    return urljoin(pdp_url, item) if item else pdp_url


def parse_window_field(h: str):
    tree = html.fromstring(html=h)

    if not len(tree.xpath('//div[@class="pdp-area"]')):
        return None

    scripts = tree.xpath('//script[contains(., "serverSideViewModel")]/text()')

    match = re.search(
        r"var\s+serverSideViewModel\s*=\s*(\{[\s\S]+?\});", scripts[0], re.DOTALL
    )

    window_data = {}
    if match:
        window_data = chompjs.parse_js_object(match.group(1))

    return window_data


def parse_pdp(h: str, reviews_json: dict, window_data: dict, pdp_url: str):
    tree = html.fromstring(html=h)

    if not len(tree.xpath('//div[@class="pdp-area"]')):
        return None

    breadcrumbs = tree.xpath(
        '//script[@type="application/ld+json" and contains(., "BreadcrumbList")]/text()'
    )
    if breadcrumbs:
        breadcrumbs = json.loads(breadcrumbs[0])

    category_tree = [
        {
            "name": el["name"],
            "url": breadcrumbs_url(el.get("item"), pdp_url),
        }
        for el in breadcrumbs["itemListElement"]
    ]

    additional_review_images = []
    customer_reviews = []

    safe_reviews_json = reviews_json.get("response") or {}
    results = safe_reviews_json.get("Results") or []

    for rev in results or []:
        photos = rev.get("Photos") or []

        for img in photos:
            sizes = img.get("Sizes") or {}
            image_data = sizes.get("large") or sizes.get("normal")

            if image_data and image_data.get("Url"):
                additional_review_images.append(urljoin(pdp_url, image_data["Url"]))

        customer_reviews.append(
            {
                "review_id": rev.get("Id"),
                "title": rev.get("Title"),
                "content": rev.get("ReviewText"),
                "min_rating": 1,
                "max_rating": 5,
                "rating": rev.get("Rating"),
            }
        )

    review_statistics = (
        (safe_reviews_json.get("Includes") or {})
        .get("Products", {})
        .get(window_data.get("code"), {})
        .get("ReviewStatistics", {})
    )

    return PDPModel.model_validate(
        {
            "breadcrumbs": category_tree,
            "name": window_data.get("displayName"),
            "url": pdp_url,
            "reviews": customer_reviews,
            "reviews_image": additional_review_images,
            "average_rating": float(
                review_statistics.get("AverageOverallRating") or 0.0
            ),
            "total_review_count": int(review_statistics.get("TotalReviewCount") or 0),
        }
    )
