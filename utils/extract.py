import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup

# Tambahkan user-agent ke dalam header
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

def extract_product_data(section):
    """Mengekstrak data produk dari satu elemen <div class='collection-card'>."""
    try:
        product_title = section.find('h3', class_='product-title').text.strip()
        price_tag = section.find('span', class_='price')
        product_price = price_tag.text.strip() if price_tag else 'Price Unavailable'

        detail_paragraphs = section.find_all('p')

        product_rating = None
        product_colors = None
        product_size = None
        product_gender = None

        for p in detail_paragraphs:
            text = p.text.strip()
            if "Rating" in text:
                product_rating = text
            elif "Colors" in text:
                product_colors = text
            elif "Size" in text:
                product_size = text
            elif "Gender" in text:
                product_gender = text

        return {
            "product_title": product_title,
            "product_price": product_price,
            "product_rating": product_rating,
            "product_colors": product_colors,
            "product_size": product_size,
            "product_gender": product_gender,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        print(f"Error saat mengekstrak data produk: {e}")
        return {
            "product_title": None,
            "product_price": None,
            "product_rating": None,
            "product_colors": None,
            "product_size": None,
            "product_gender": None,
            "timestamp": datetime.now().isoformat()
        }

def fetch_page_content(url):
    """Mengambil konten HTML dari URL dengan user-agent yang ditentukan."""
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()  # Memunculkan HTTPError jika status buruk
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error saat mengambil {url}: {e}")
        return None

def scrape_product_data(url):
    """Melakukan scraping untuk semua data produk."""
    try:
        content = fetch_page_content(url)
        if not content:
            return []

        soup = BeautifulSoup(content, 'html.parser')
        data = []

        articles = soup.find_all('div', class_='collection-card')

        for article in articles:
            product_data = extract_product_data(article)
            data.append(product_data)
            
        return data
    except Exception as e:
        print(f"Error saat melakukan scraping pada {url}: {e}")
        return []