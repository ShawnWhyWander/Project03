# Project03 - ebay-dl.py

## Overview

This project is a simple eBay web scraper that collects the first 10 search results for any given search term and stores the results in a `.json` file.

Each item dictionary in the JSON includes:
- `name`: The item name
- `price`: The price in cents (integer)
- `status`: Item condition (e.g., "Brand New", "Pre-Owned")
- `shipping`: Shipping cost in cents (0 if free)
- `free_returns`: Boolean indicating free returns
- `items_sold`: Number of items sold (if listed)

---

## How to Run and Save JSON Files

Make sure you have Python 3 and the required libraries installed:

```bash
pip install requests beautifulsoup4
python ebay-dl.py "claremont mckenna"
python ebay-dl.py "macbook"
python ebay-dl.py "golf club"
```

## How to Run and Save CSV Files
```bash
python ebay-dl.py "claremont mckenna" --csv
python ebay-dl.py "macbook" --csv
python ebay-dl.py "golf club" --csv
```

link to the course project [Project03](https://github.com/mikeizbicki/cmc-csci040/tree/2025spring/project_03_webscraping#project-3-scraping-from-ebay)