import pandas as pd
import unittest
from unittest import TestCase
from unittest.mock import patch, MagicMock, mock_open
from utils.load import load_to_csv, load_to_gsheets, load_to_postgre

class TestLoad(TestCase):
    def setUp(self):
        self.df = pd.DataFrame(
            {'product_title':'Pants', 'product_price':'$121.00', 'product_rating':'Rating: 4.2 / 5', 'product_colors':'4 Colors', 'product_size':'Size: M', 'product_gender':'Gender: Unisex'},
            {'product_title':'Crewneck', 'product_price':'$150.00', 'product_rating':'Rating: 4.8 / 5', 'product_colors':'5 Colors', 'product_size':'Size: M', 'product_gender':'Gender: Women'}
        )

    @patch('utils.load.pd.DataFrame.to_csv')
    def test_load_to_csv(self, mock_to_csv):
        """Test fungsi untuk menyimpan data ke CSV."""
        load_to_csv(self.df, "products_fashion.csv")
        mock_to_csv.assert_called_once_with("products_fashion.csv", index=False)

    @patch("utils.load.build")
    @patch("utils.load.Credentials.from_service_account_file")
    def test_load_to_gsheets(self, mock_creds, mock_build):
        """Test fungsi untuk menyimpan data ke gsheets"""
        mock_creds.return_value = MagicMock()
        mock_service = MagicMock()
        mock_build.return_value = mock_service

        load_to_gsheets(self.df, "spreadsheet_id", "Sheet1!A1")

        mock_build.assert_called_once()
        mock_creds.assert_called_once_with('etl-project-cc25.json')
        mock_service.spreadsheets.return_value.values.return_value.update.assert_called_once()

    @patch("pandas.DataFrame.to_sql")
    @patch("utils.load.create_engine")
    def test_load_to_postgre(self, mock_engine, m_to_sql):
        mock_conn = mock_engine.return_value.connect.return_value.__enter__.return_value

        load_to_postgre(self.df, "postgresql+psycopg2://developer:supersecretpassword@localhost:5432/fashionproddb")
        mock_engine.assert_called_once_with("postgresql+psycopg2://developer:supersecretpassword@localhost:5432/fashionproddb")

        m_to_sql.assert_called_once_with('fashion_product',con=mock_conn,if_exists='append',index=False)
