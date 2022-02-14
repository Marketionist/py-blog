#!/usr/bin/python

# SERVER_NAME='yourdomain.org' python freeze.py

from flask_frozen import Freezer
from server import app
import os
import sys
sys.path.append(os.path.abspath('utils'))
from utils import parser

app.config.update(
    FREEZER_IGNORE_404_NOT_FOUND=True,
)

freezer = Freezer(app)

parsed_posts = parser.parse_posts()

@freezer.register_generator
def show_html_page (): # Endpoint defaults to the function name
    # Values dicts
    yield {'page_name': '404'}
    yield {'page_name': 'about'}
    yield {'page_name': 'elements'}
    yield {'page_name': 'generic'}

@freezer.register_generator
def show_post_html_page (): # Endpoint defaults to the function name
    # Values dicts
    for post in parsed_posts:
        yield {
            'category_name': post['category_name'],
            'page_name': post['page_name']
        }

if __name__ == '__main__':
    freezer.freeze()
