import json
import time
import requests
from bs4 import BeautifulSoup

base_url = "https://www.jumia.com.ng"
endpoint = "/catalog/productratingsreviews/sku/SK821HA1HROXDNAFAMZ/"


proxy_host = "new-york1.thesocialproxy.com"
proxy_port = 10000
proxy_username = "ksbvinh5u6jmf8wt"
proxy_password = "c5kxhtqil4mw9b1o"

proxy = {
    "http": f"http://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}",
    "https": f"http://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}",
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
}


def get_next_page_url(soup):
    next_page = soup.find("a", {"aria-label": "Next Page"})
    if next_page:
        return next_page["href"]
    return None


# Function to scrape multiple pages
def scrape_reviews(url):

    total_data = []

    try:
        while url:
            response = requests.get(
                base_url + url, proxies=proxy, headers=headers, timeout=120
            )

            soup = BeautifulSoup(response.text, "html.parser")

            # Scrape reviews and ratings for the current page
            reviews = soup.find_all("article", class_="-pvs")
            for review in reviews:
                rating_div = review.find("div", class_="stars")
                rating_text = rating_div.text.strip().split(" ")[0]
                review_text = review.find("p", class_="-pvs").text.strip()

                total_data.append({"rating": rating_text, "review": review_text})

            # Get the URL for the next page
            next_page_url = get_next_page_url(soup)
            if next_page_url:
                url = next_page_url
            else:
                break

            active_page = soup.find("a", class_="pg _act")
            if active_page:
                current_page = active_page.text.strip()
                print(f"Done with page: {current_page}")
            else:
                print("Done with page...")

            time.sleep(3)

    except Exception as e:
        print(e)
        with open("data.json", "w", encoding="utf-8") as file:
            json.dump(total_data, file, indent=4)

    finally:
        with open("data.json", "w", encoding="utf-8") as file:
            json.dump(total_data, file, indent=4)

# Start scraping from the first page
scrape_reviews(endpoint)
