import pandas as pd
import numpy as np

def replace_invalid_values(df):
    """Mengganti nilai tidak valid pada kolom tertentu dengan NaN."""
    # Product Rating
    try:
        df['product_rating'] = df['product_rating'].replace({
            'Rating: ⭐ Invalid Rating / 5': np.nan,
            'Rating: Not Rated': np.nan
        })
    except Exception as e:
        print(f"Error replacing product_rating: {e}")

    # Product Price
    try:
        df['product_price'] = df['product_price'].replace({
            'Price Unavailable': np.nan,
        })
    except Exception as e:
        print(f"Error replacing product_price: {e}")

    # Product Title
    try:
        df['product_title'] = df['product_title'].replace({
            'Unknown Product': np.nan,
        })
    except Exception as e:
        print(f"Error replacing product_title: {e}")
    
    return df

def transform_data(df, exchange_rate):
    """Menggabungkan semua transformasi data menjadi satu fungsi."""

    # Replace Invalid Data with NaN
    df = replace_invalid_values(df)

    # Transform Product Price
    try:
        df['product_price'] = df['product_price'].astype(str).str.replace(r'[$,]', '', regex=True).astype(float)
        df['product_price'] = (df['product_price'] * exchange_rate).astype(float)
    except Exception as e:
        print(f"Error transforming product_price: {e}")

    # Transform Product Rating
    try:
        df['product_rating'] = df['product_rating'].str.split(":").str[-1].str.strip()
        df['product_rating'] = df['product_rating'].str.extract(r'(\d+\.\d+)').astype(float)
    except Exception as e:
        print(f"Error transforming product_rating: {e}")

    # Transform Product Size
    try:
        df['product_size'] = df['product_size'].str.split(":").str[-1].str.strip()
    except Exception as e:
        print(f"Error transforming product_size: {e}")

    # Transform Product Gender
    try:
        df['product_gender'] = df['product_gender'].str.split(":").str[-1].str.strip()
    except Exception as e:
        print(f"Error transforming product_gender: {e}")

    # Transform Product Colors
    try:
        df['product_colors'] = df['product_colors'].str.extract(r'(\d+)').astype('int64')
    except Exception as e:
        print(f"Error transforming product_colors: {e}")

    # Drop Missing Values
    df = df.dropna()

    # Drop Duplicates
    df = df.drop_duplicates()

    return df