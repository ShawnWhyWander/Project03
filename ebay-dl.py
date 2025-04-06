import argparse
import requests
from bs4 import BeautifulSoup
import json
import re
import time
from urllib.parse import urljoin

# Setup argparse
parser = argparse.ArgumentParser(description="Download eBay search results")
parser.add_argument("search_term", help="Search term for eBay")
args = parser.parse_args()
search_term = args.search_term

# Starting URL
base_url = "https://www.ebay.com/sch/i.html"
current_url = f"{base_url}?_nkw={search_term}"

# Request headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9"
}

items = []
page = 1
max_pages = 5

# Loop through result pages
while page <= max_pages:
    print(f"Scraping page {page}...")

    response = requests.get(current_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    listings = soup.select(".s-item")

    if not listings:
        print("No listings found.")
        break

    for item in listings:
        name_tag = item.select_one(".s-item__title")
        price_tag = item.select_one(".s-item__price")
        status_tag = item.select_one(".SECONDARY_INFO")
        shipping_tag = item.select_one(".s-item__shipping, .s-item__freeXDays")
        free_returns_tag = item.select_one(".s-item__free-returns")
        sold_tag = item.select_one(".s-item__hotness, .s-item__additionalItemHotness")

        name = name_tag.get_text(strip=True) if name_tag else None

        # Extract price in cents
        price = None
        if price_tag:
            match = re.search(r"\$([\d,]+(\.\d{2})?)", price_tag.get_text())
            if match:
                price = int(float(match.group(1).replace(",", "")) * 100)

        status = status_tag.get_text(strip=True) if status_tag else None

        # Extract shipping in cents
        shipping = None
        if shipping_tag:
            shipping_text = shipping_tag.get_text()
            if "Free shipping" in shipping_text:
                shipping = 0
            else:
                match = re.search(r"\$([\d,]+(\.\d{2})?)", shipping_text)
                if match:
                    shipping = int(float(match.group(1).replace(",", "")) * 100)

        free_returns = free_returns_tag is not None

        # Extract items sold
        items_sold = None
        if sold_tag:
            match = re.search(r"(\d+(,\d+)*) sold", sold_tag.get_text())
            if match:
                items_sold = int(match.group(1).replace(",", ""))

        item_dict = {
            "name": name,
            "price": price,
            "status": status,
            "shipping": shipping,
            "free_returns": free_returns,
            "items_sold": items_sold
        }

        items.append(item_dict)

    # Go to next page
    next_link = soup.select_one("a.pagination__next")
    if next_link and "href" in next_link.attrs:
        current_url = urljoin("https://www.ebay.com", next_link["href"])
        page += 1
        time.sleep(1)
    else:
        break  # No next page found

# Save to JSON
filename = f"{search_term.replace(' ', '_')}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(items, f, indent=2)

print(f"Scraped {len(items)} items. Saved to {filename}.")
