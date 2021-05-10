# py-blog

A simple static blog template

## Requirements
Python versions: 2.7 or 3.5+

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
To run the server:
```bash
FLASK_APP=server.py FLASK_ENV=development flask run
```
To freeze the app:
```bash
python freeze.py
```

## Thanks
If this script was helpful to you, please give it a **★ Star** on
[GitHub](https://github.com/Marketionist/py-blog)
