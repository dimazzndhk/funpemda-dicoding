from utils.extract import extract_product_data, fetch_page_content, scrape_product_data
from bs4 import BeautifulSoup
import unittest
from unittest import TestCase
from unittest.mock import patch, Mock
import requests

class TestExtract(TestCase):
    """Unit test untuk fungsi-fungsi pada extract.py."""

    def setUp(self):
        self.valid_html = '''
        <div class="collection-card">
                        <div style="position: relative;">
                            <img src="https://picsum.photos/280/350?random=2" class="collection-image" alt="T-shirt 2">
                            
                        </div>
                        <div class="product-details">
                            <h3 class="product-title">T-shirt 2</h3>
                            <div class="price-container"><span class="price">$102.15</span></div>
                            <p style="font-size: 14px; color: #777;">Rating: ⭐ 3.9 / 5</p>
                            <p style="font-size: 14px; color: #777;">3 Colors</p>
                            <p style="font-size: 14px; color: #777;">Size: M</p>
                            <p style="font-size: 14px; color: #777;">Gender: Women</p>
                        </div>
                    </div>
        '''

        self.invalid_html = '''
        <div class="collection-card">
            <h2 class="product-title"></h2>
        </div>
        '''

    def test_extract_product_data(self):
        """test untuk fungsi extract data product"""
        soup = BeautifulSoup(self.valid_html, 'html.parser')
        section = soup.find('div', class_='collection-card')
        data = extract_product_data(section)

        self.assertEqual(data['product_title'], "T-shirt 2")
        self.assertEqual(data['product_price'], "$102.15")
        self.assertIn("Rating: ⭐ 3.9 / 5", data['product_rating'])
        self.assertEqual(data['product_colors'], "3 Colors")
        self.assertEqual(data['product_size'], "Size: M")
        self.assertEqual(data['product_gender'], "Gender: Women")
        self.assertIsInstance(data['timestamp'], str)
    
    def test_extract_product_data_error(self):
        soup = BeautifulSoup(self.invalid_html, 'html.parser')
        section = soup.find('div', class_='collection-card')
        data = extract_product_data(section)
    
    @patch('utils.extract.requests.get')
    def test_fetch_page_content(self, mock_get):
        """test untuk fungsi fetch page content"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'<html></html>'
        mock_get.return_value = mock_response

        url = 'https://fashion-studio.dicoding.dev'
        result = fetch_page_content(url)
        self.assertEqual(result, b'<html></html>')

    @patch('utils.extract.requests.get')
    def test_fetch_page_content_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Connection error")
        url = 'https://fashion-studio.dicoding.dev'
        result = fetch_page_content(url)
        self.assertIsNone(result)
    
    @patch('utils.extract.fetch_page_content')
    def test_scrape_product_data(self, mock_fetch):
        """test untuk fungsi scrape data product"""
        html = '''
        <html>
            <div class="collection-card">
                        <div style="position: relative;">
                            <img src="https://picsum.photos/280/350?random=2" class="collection-image" alt="T-shirt 2">
                            
                        </div>
                        <div class="product-details">
                            <h3 class="product-title">T-shirt 2</h3>
                            <div class="price-container"><span class="price">$102.15</span></div>
                            <p style="font-size: 14px; color: #777;">Rating: ⭐ 3.9 / 5</p>
                            <p style="font-size: 14px; color: #777;">3 Colors</p>
                            <p style="font-size: 14px; color: #777;">Size: M</p>
                            <p style="font-size: 14px; color: #777;">Gender: Women</p>
                        </div>
                    </div>
        </html>
        '''
        mock_fetch.return_value = html
        url = 'https://fashion-studio.dicoding.dev'
        result = scrape_product_data(url)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['product_title'], "T-shirt 2")
        self.assertIn("Rating", result[0]['product_rating'])
        self.assertIn("Size", result[0]['product_size'])
        self.assertIn("Gender", result[0]['product_gender'])