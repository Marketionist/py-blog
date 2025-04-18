#!/usr/bin/python

import os
import markdown
import markdown.extensions.fenced_code
import datetime

domain_name = os.getenv('SERVER_NAME')
url_scheme = 'https'

def parse_posts():
    posts = []

    for root, dirs, files in os.walk('posts'):
        for file_name in files:
            if file_name.endswith('.md') and not 'main-page' in file_name and not '_draft' in file_name:
                try:
                    file_path = os.path.join(root, file_name)
                    with open(file_path, mode='r') as my_file:
                        text = my_file.read()
                        text_split_in_10 = text.split('\n', 9)

                        post_title = text_split_in_10[1].replace('title: ', '')
                        post_description = text_split_in_10[2].replace('description: ', '')
                        post_keywords = text_split_in_10[3].replace('keywords: ', '')
                        # Considering date is in yyyy-mm-dd hh:mm:ss format
                        post_date = datetime.datetime.strptime(
                            text_split_in_10[6].replace('date: ', ''),
                            '%Y-%m-%d %H:%M:%S'
                        )
                        post_html_content = markdown.markdown(
                            text_split_in_10[9],
                            extensions=['fenced_code']
                        )
                except FileNotFoundError as err:
                    raise Exception(f'File doesn\'t exist - {err}') from err
                except IOError as err:
                    raise Exception(f'Input/Output error - {err}') from err
                except ValueError as err:
                    raise Exception(f'Something wrong with the top section paramters of {file_path} - {err}') from err

                category_name = root.replace('posts/', '')
                domain_url = url_scheme + '://' + (domain_name or '127.0.0.1:5000')

                post = {
                    'category_name': category_name,
                    'page_name': file_name.replace('.md', ''),
                    'url': os.path.join(domain_url, category_name, file_name).replace('.md', '.html'),
                    'title': post_title,
                    'description': post_description,
                    'keywords': post_keywords,
                    'date': post_date,
                    'last_modified': str(datetime.datetime.date(post_date)) + 'T' + str(datetime.datetime.time(post_date)) + '+00:00',
                    'html_content': post_html_content,
                    'image': os.path.join(
                        '../', 'static', 'images', category_name, file_name.replace('.md', '.jpg')
                    ),
                }
                if not post in posts:
                    posts.append(post)
    return posts
