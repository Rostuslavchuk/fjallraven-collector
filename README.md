# Fjällräven Product Collector

An asynchronous web scraper for extracting product data from the [Fjällräven](https://www.fjallraven.com/) website.

The collector combines HTTP requests and browser automation to retrieve product information from dynamic product pages and collect customer reviews through the website's API.

## Features

- Product URL discovery and collection.
- Dynamic page rendering using Playwright.
- Asynchronous HTTP requests using `curl_cffi`.
- Browser context and cookie management.
- Product data extraction from HTML and JavaScript data.
- Customer reviews collection through the Reviews API.
- Data validation using Pydantic.
- Structured JSON output.
- Error logging and request status monitoring.

## Tech Stack

- **Python** — primary programming language.
- **asyncio** — asynchronous execution.
- **Playwright** — browser automation and dynamic content rendering.
- **curl_cffi** — asynchronous HTTP requests with browser impersonation.
- **lxml** — HTML parsing and XPath selectors.
- **Pydantic** — data validation and serialization.

## Project Structure

```text
fjallraven_collector/
├── config/
│   └── headers.py
├── fetcher/
│   └── fetcher.py
├── models/
│   └── models.py
├── parser/
│   └── pdp_parser.py
├── storage/
│   └── storage.py
├── utils/
│   └── logger.py
├── main.py
└── requirements.txt
```

## Data Extraction

The collector retrieves product information such as:

- Product name
- Product URL
- Product description
- Price
- Images
- Breadcrumbs
- Product variants
- Customer reviews

Data is validated using Pydantic models and exported to JSON.

## Execution

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Playwright Chromium:

```bash
playwright install chromium
```

Sitemap collection:

```bash
python -m piplines.discovery_pipline -u https://www.fjallraven.com/us/en-us/Sitemap.xml
```

Pdp collection:

```bash
python -m pipelines.pdp_pipline
```

Collected data store at: storage/pdp_data.json

## Architecture

The collector uses two complementary data retrieval mechanisms:

1. **Playwright** — loads product pages and renders JavaScript-dependent content.
2. **curl_cffi** — handles asynchronous API requests for customer reviews.

This approach allows the collector to retrieve data from both dynamically rendered pages and dedicated API endpoints.

## Output

Collected data is stored in structured JSON files for further processing and analysis.

---

**Project:** Fjällräven Product Collector  
**Language:** Python 3.14+
