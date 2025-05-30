from utils.extract import scrape_product_data
from utils.transform import transform_data
from utils.load import load_to_csv, load_to_postgre, load_to_gsheets
import pandas as pd

def main():
    """Fungsi utama untuk menjalankan proses scraping dari semua halaman dan menyimpan data."""
    base_url = 'https://fashion-studio.dicoding.dev'
    all_data = []

    # Scrape halaman pertama 
    first_page_data = scrape_product_data(base_url)
    all_data.extend(first_page_data)

    # Scrape next page
    for page_num in range(2, 51):
        page_url = f'{base_url}/page{page_num}'
        page_data = scrape_product_data(page_url)
        if page_data:
            all_data.extend(page_data)
        else:
            print(f"Tidak ada data pada page {page_num}")

    # Result
    if all_data:
        try:
            df = pd.DataFrame(all_data)
            df = transform_data(df, 16000)
            print(df)

            # Menyimpan data
            load_to_csv(df, filename="products_fashion.csv")
            load_to_gsheets(df, spreadsheet_id='xxspreadsheet_idxx', range_name='Sheet1!A1')
            db_url='xxdb_urlxx'
            load_to_postgre(df, db_url)
        except Exception as e:
            print(f"Terjadi kesalahan dalam proses: {e}")
    else:
        print("Tidak ada data yang ditemukan.")

if __name__ == "__main__":
    main()