import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from sqlalchemy import create_engine

def load_to_csv(df, filename="products.csv"):
    """Menyimpan data dengan format CSV."""
    try:
        df.to_csv(filename, index=False)
        print(f"Data berhasil disimpan ke {filename}.")
    except Exception as e:
        print(f"Error load data to CSV: {e}")

def load_to_gsheets(df, spreadsheet_id, range_name):
    """Menyimpan data ke Google Sheets."""
    try:
        creds = Credentials.from_service_account_file('etl-project-cc25.json') 
        service = build('sheets', 'v4', credentials=creds) 
        sheet = service.spreadsheets() 
        
        # Mengonversi DataFrame ke list 
        values = [df.columns.tolist()] + df.values.tolist()
        body = {'values': values}
        
        # Mengirim data ke Google Sheets
        sheet.values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='RAW',
            body=body
        ).execute()
        
        print(f"Data berhasil disimpan ke Google Sheets.")
    
    except Exception as e:
        print(f"Error load data to Google Sheets: {e}")

def load_to_postgre(df, db_url):
    """Menyimpan DataFrame ke dalam PostgreSQL."""
    try:
        # Membuat engine database
        engine = create_engine(db_url)
        
        # Menyimpan data ke tabel 'fashion_product' jika tabel sudah ada, data akan ditambahkan (append)
        with engine.connect() as con:
            df.to_sql('fashion_product', con=con, if_exists='append', index=False)
            print("Data berhasil ditambahkan ke PostgreSQL")
    
    except Exception as e:
        print(f"Error load data to PostgreSQL: {e}")