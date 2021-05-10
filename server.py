#!/usr/bin/python

# FLASK_APP=server.py FLASK_ENV=development flask run

# pip install -r requirements.txt

# pip install markdown Frozen-Flask && pip freeze > requirements.txt

import os
import csv
import markdown
import markdown.extensions.fenced_code
from flask import Flask, render_template, url_for, request, redirect, send_from_directory

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found (error):
   return render_template('404.html', title='404'), 404

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
        return render_template(f'{page_name}.html')
    else:
        return render_template('404.html', title='404'), 404

@app.route('/<string:category_name>/<string:page_name>.html')
def show_post_html_page (category_name, page_name):
    try:
        with open(os.path.join(
            'posts', category_name, f'{page_name}.md'
        ), mode='r') as my_file:
            text = my_file.read()
            text_split_in_4 = text.split('\n', 3)

            post_description = text_split_in_4[0]
            post_keywords = text_split_in_4[1]
            post_title = text_split_in_4[2].replace('# ', '')

            post_html_content = markdown.markdown(
                text_split_in_4[2] + text_split_in_4[3],
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

if __name__ == "__main__":
    app.run()
