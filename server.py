#!/usr/bin/python

# FLASK_APP=server.py FLASK_ENV=development flask run

# pip install -r requirements.txt

# pip install markdown Frozen-Flask && pip freeze > requirements.txt

import os
import csv
import markdown
import markdown.extensions.fenced_code
import datetime
from flask import Flask, render_template, url_for, request, redirect, send_from_directory

app = Flask(__name__)

domain_name = os.getenv('SERVER_NAME')

app.config.update(
    SERVER_NAME=domain_name,
    PREFERRED_URL_SCHEME='https',
)

@app.errorhandler(404)
def page_not_found (error):
   return render_template('404.html', title='404'), 404

@app.route('/robots.txt')
def show_robots_txt ():
    return render_template('robots.txt', domain=domain_name)

@app.route('/')
def my_home ():
    try:
        with open(os.path.join('posts', 'post-1.md'), mode='r') as my_file:
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
    try:
        with open(os.path.join(
            'posts', category_name, f'{page_name}.md'
        ), mode='r') as my_file:
            text = my_file.read()
            text_split_in_10 = text.split('\n', 9)

            post_title = text_split_in_10[1].replace('title: ', '')
            post_description = text_split_in_10[2].replace('description: ', '')
            post_keywords = text_split_in_10[3].replace('keywords: ', '')
            post_date = text_split_in_10[6].replace('date: ', '')

            post_html_content = markdown.markdown(
                text_split_in_10[9],
                extensions=['fenced_code']
            )
    except FileNotFoundError as err:
        print(f'File doesn\'t exist - {err}')
        return render_template('404.html'), 404
    except IOError as err:
        print(f'Input/Output error - {err}')
        raise err

    return render_template(
        'post.html',
        title=post_title,
        description=post_description,
        keywords=post_keywords,
        image=os.path.join(
            '../', 'static', 'images', category_name, f'{page_name}.jpg'
        ),
        content=post_html_content
    )

@app.context_processor
def inject_current_time():
    return { 'current': datetime.datetime.today() }


if __name__ == "__main__":
    app.run()
