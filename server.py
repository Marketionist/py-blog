#!/usr/bin/python

# FLASK_APP=server.py FLASK_ENV=development flask run

# pip install -r requirements.txt

# pip install markdown Frozen-Flask && pip freeze > requirements.txt

import os
import sys
import csv
import markdown
import markdown.extensions.fenced_code
import datetime
from flask import Flask, render_template, url_for, request, redirect, send_from_directory

sys.path.append(os.path.abspath('/utils'))
from utils import parser

app = Flask(__name__)

domain_name = os.getenv('SERVER_NAME')
url_scheme = 'https'

app.config.update(
    SERVER_NAME=domain_name,
    PREFERRED_URL_SCHEME=url_scheme,
)

parsed_posts = parser.parse_posts()

# Context processors to inject new variables automatically into the context of
# a template
# https://flask.palletsprojects.com/en/1.0.x/templating/#context-processors
@app.context_processor
def inject_current_time():
    return { 'current': datetime.datetime.today() }

@app.context_processor
def inject_posts_array():
    return { 'posts_array': sorted(parsed_posts, key=lambda x: x['date'], reverse=True) }

# Routes
@app.errorhandler(404)
def page_not_found (error):
   return render_template('404.html', title='404'), 404

@app.route('/robots.txt')
def show_robots_txt ():
    return render_template('robots.txt', domain=domain_name)

@app.route('/')
def my_home ():
    try:
        with open(os.path.join('posts', 'main-page.md'), mode='r') as my_file:
            text = my_file.read()
            post_html_content = markdown.markdown(
                text, extensions=['fenced_code']
            )
    except FileNotFoundError as err:
        print(f'File doesn\'t exist - {err}')
        raise err
    except IOError as err:
        print(f'Input/Output error - {err}')
        raise err

    return render_template('index.html', content=post_html_content)

@app.route('/<string:page_name>.html')
def show_html_page (page_name):
    if page_name != 'index':
        try:
            return render_template(f'{page_name}.html')
        except Exception as err:
            print(f'File doesn\'t exist - {err}')
            return render_template('404.html', title='404'), 404
    else:
        return render_template('404.html', title='404'), 404

@app.route('/<string:category_name>/<string:page_name>.html')
def show_post_html_page (category_name, page_name):
    post_path = os.path.join(category_name, f'{page_name}.html')

    try:
        # Filter all posts that have post_path in url and return first of those
        matching_post = list(filter(lambda x: post_path in x['url'], parsed_posts))[0]

        if matching_post:
            return render_template(
                'post.html',
                title=matching_post['title'],
                description=matching_post['description'],
                keywords=matching_post['keywords'],
                image=matching_post['image'],
                content=matching_post['html_content']
            )
    except IndexError as err:
        print(f'File doesn\'t exist')
        return render_template('404.html'), 404


if __name__ == "__main__":
    app.run()
