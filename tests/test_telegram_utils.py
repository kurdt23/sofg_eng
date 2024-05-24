import unittest
from unittest.mock import patch
import sys
import os

# Добавляем путь к родительской директории
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from telegram_utils import send_photo, send_message


class TestTelegramUtils(unittest.TestCase):
    @patch('requests.post')
    def test_send_photo(self, mock_post):
        send_photo('dummy_token', 'dummy_chat_id', 'dummy_path')
        self.assertTrue(mock_post.called)

    @patch('requests.get')
    def test_send_message(self, mock_get):
        send_message('dummy_token', 'dummy_chat_id', 'dummy_message')
        self.assertTrue(mock_get.called)