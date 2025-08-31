# py-blog

A simple static blog template.

## Requirements
Python versions: 2.7 or 3.5+.

## Installation
1. Clone this repository:
```bash
git clone https://github.com/Marketionist/py-blog.git
```
2. Create virtual environment and activate it:
```bash
python -m venv py-blog/
source py-blog/bin/activate
```
3. Switch to py-blog folder and install all dependencies:
```bash
cd py-blog && pip install -r requirements.txt
```

## Running
### To run the server
```bash
FLASK_APP='server.py' FLASK_ENV='development' flask run
```
The server will start running on http://127.0.0.1:5000/ (Press CTRL+C to quit).
Or if you want to enable auto-update mode:
```bash
FLASK_APP='server.py' FLASK_ENV='development' FLASK_DEBUG=1 flask run
```

### To freeze the app
1. Add the articles as markdown `.md` files to the `posts/{post-category}`
folder. Here is a good
[Markdown Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet).
Corresponding URL will be generated from each article file name.
2. Add images for each article to `static/images/{post-category}` folder.
3. Generate the static files:
```bash
SERVER_NAME='yourdomain.org' python freeze.py
```
> All generated files will appear inside the `build` folder. Copy generated
> files to your hosting.
4. To copy all folders and files one level up from the `build` folder:
```bash
cp -r build/* .
```

## Thanks
If this script was helpful to you, please give it a **★ Star** on
[GitHub](https://github.com/Marketionist/py-blog).
