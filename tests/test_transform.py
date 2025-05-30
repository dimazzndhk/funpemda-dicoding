from utils.transform import replace_invalid_values, transform_data
import unittest
from unittest import TestCase
from unittest.mock import patch
import pandas as pd

class TestTransform(TestCase):
    """Unit test untuk fungsi-fungsi pada transform.py."""
    
    def test_replace_invalid_values(self):
        """test untuk mengganti invalid values dengan np.nan"""
        # data dummy untuk pengujian
        products_fashion = [
            {'product_title':'Hoodie', 'product_price':'$100.00', 'product_rating':'Rating: ⭐ Invalid Rating / 5', 'product_colors':'3 Colors', 'product_size':'Size: XXL', 'product_gender':'Gender: Men'},
            {'product_title':'Jacket', 'product_price':'Price Unavailable', 'product_rating':'Rating: 4.5 / 5', 'product_colors':'2 Colors', 'product_size':'Size: S', 'product_gender':'Gender: Unisex'},
            {'product_title':'Unknown Product', 'product_price':'$100.00', 'product_rating':'Rating: Not Rated', 'product_colors':'1 Colors', 'product_size':'Size: M', 'product_gender':'Gender: Men'}
        ]

        df = pd.DataFrame(products_fashion)
        df = replace_invalid_values(df)

        # Validasi jumlah baris
        self.assertEqual(df.isnull().any(axis=1).sum(), 3)
    
    def test_transform_data(self):
        """test untuk transformasi atau cleaning data"""
        # data dummy untuk pengujian
        products_fashion = [
            {'product_title':'Hoodie', 'product_price':'$100.00', 'product_rating':'Rating: ⭐ Invalid Rating / 5', 'product_colors':'3 Colors', 'product_size':'Size: XXL', 'product_gender':'Gender: Men'},
            {'product_title':'Jacket', 'product_price':'Price Unavailable', 'product_rating':'Rating: 4.5 / 5', 'product_colors':'2 Colors', 'product_size':'Size: S', 'product_gender':'Gender: Unisex'},
            {'product_title':'Unknown Product', 'product_price':'$100.00', 'product_rating':'Rating: Not Rated', 'product_colors':'1 Colors', 'product_size':'Size: M', 'product_gender':'Gender: Men'},
            {'product_title':'Pants', 'product_price':'$121.00', 'product_rating':'Rating: 4.2 / 5', 'product_colors':'4 Colors', 'product_size':'Size: M', 'product_gender':'Gender: Unisex'},
            {'product_title':'Crewneck', 'product_price':'$150.00', 'product_rating':'Rating: 4.8 / 5', 'product_colors':'5 Colors', 'product_size':'Size: M', 'product_gender':'Gender: Women'}
        ]

        exchange_rate = 16000
        df = pd.DataFrame(products_fashion)
        df_cleaned = transform_data(df, exchange_rate)

        # Validasi jumlah baris
        self.assertEqual(len(df_cleaned), 2)

        # Validasi nilai data
        # Baris ke-0
        self.assertEqual(df_cleaned.iloc[0]['product_title'], 'Pants')
        self.assertAlmostEqual(df_cleaned.iloc[0]['product_price'], 121.00 * exchange_rate)
        self.assertAlmostEqual(df_cleaned.iloc[0]['product_rating'], 4.2)
        self.assertEqual(df_cleaned.iloc[0]['product_colors'], 4)
        self.assertEqual(df_cleaned.iloc[0]['product_size'], 'M')
        self.assertEqual(df_cleaned.iloc[0]['product_gender'], 'Unisex')

        # Baris ke-1
        self.assertEqual(df_cleaned.iloc[1]['product_title'], 'Crewneck')
        self.assertEqual(df_cleaned.iloc[1]['product_price'], 150.00 * exchange_rate)
        self.assertEqual(df_cleaned.iloc[1]['product_rating'], 4.8)
        self.assertEqual(df_cleaned.iloc[1]['product_colors'], 5)
        self.assertEqual(df_cleaned.iloc[1]['product_size'], 'M')
        self.assertEqual(df_cleaned.iloc[1]['product_gender'], 'Women')

        # Validasi kolom
        expected_columns = ['product_title', 'product_price', 'product_rating', 'product_colors', 'product_size', 'product_gender']
        for col in expected_columns:
            self.assertIn(col, df.columns)
    
    def test_transform_data_error(self):
        # data dummy untuk pengujian
        products_fashion = [
            {'product_title':'Hoodie', 'product_price':'100.00 dollar', 'product_rating':'Rating: ⭐ Invalid Rating / 5', 'product_colors':'3 Colors', 'product_size':'Size: XXL', 'product_gender':'Gender: Men'},
            {'product_title':'Jacket', 'product_price':'Price Unavailable', 'product_rating':'Rating: 4.5 / 5', 'product_colors':'2 Colors', 'product_size':'Size: S', 'product_gender':'Gender: Unisex'},
            {'product_title':'Unknown Product', 'product_price':'$100.00', 'product_rating':'Rating: Not Rated', 'product_colors':'1 Colors', 'product_size':'Size: M', 'product_gender':'Gender: Men'},
            {'product_title':'Pants', 'product_price':'$121.00', 'product_rating':'Rating Good', 'product_colors':'Four Colors', 'product_size':'Size: M', 'product_gender':'Gender: Unisex'},
            {'product_title':'Crewneck', 'product_price':'$150.00', 'product_rating':'Rating: 4.8 / 5', 'product_colors':'5 Colors', 'product_size':'SizeM', 'product_gender':'Gender: Women'}
        ]

        exchange_rate = 16000
        df = pd.DataFrame(products_fashion)
        df.drop(columns=['product_rating'], inplace=True)
        df_cleaned = transform_data(df, exchange_rate)