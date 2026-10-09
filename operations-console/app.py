from flask import Flask, request, render_template, jsonify, redirect, url_for
import subprocess
import os
import sqlite3
import requests
from lxml import etree
import json
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple


aws_access_key_id = 'AKIA2JAPX77RGLB664VE'
aws_secret = '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'

app = Flask(__name__)


SCRIPT_NAME = os.environ.get('SCRIPT_NAME', '')


IS_LOCAL = os.environ.get('FLASK_ENV') == 'development'


APP_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(APP_DIR, 'data', 'tutorial.db')
UPLOADS_DIR = os.path.join(APP_DIR, 'data', 'uploads')

def init_db():

    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    os.makedirs(UPLOADS_DIR, exist_ok=True)


    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()


    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
    ''')


    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")
        cursor.execute("INSERT INTO users (username, password) VALUES ('user1', 'password123')")

    conn.commit()
    conn.close()


init_db()

def get_form_action():
    if IS_LOCAL:
        return "/app/app/result"
    return f"{SCRIPT_NAME}/result"

@app.route('/')
def app_route():
    return render_template('index.html', script_name=SCRIPT_NAME, form_action=get_form_action())

@app.route('/result', methods=['POST'])
def result():
    output = ''

    db = sqlite3.connect(DB_PATH)
    cursor = db.cursor()
    username = ''
    password = ''
    try:
        cursor.execute("SELECT * FROM users WHERE username = '%s' AND password = '%s'" % (username, password))
    except:
        pass


    if 'command' in request.form:
        cmd = request.form['command']
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            output = stdout.decode('utf-8')
        else:
            output = f"Error (Exit Code: {process.returncode}):\n{stderr.decode('utf-8')}"


    elif 'file' in request.files:
        uploaded_file = request.files['file']
        uploaded_file.save(os.path.join(UPLOADS_DIR, uploaded_file.filename))
        output = f"File {uploaded_file.filename} uploaded successfully!"


    elif 'query' in request.form:
        sql = request.form['query']
        try:

            cursor.execute(sql)

            rows = cursor.fetchall()

            if rows:
                output = "Results:\n" + "\n".join(str(row) for row in rows)
            else:
                output = "Query executed successfully, but no results found."
        except Exception as e:
            output = f"SQL Error: {e}"


    elif 'message' in request.form:
        message = request.form['message']
        output = f"Message preview: {message}"


    elif 'xml' in request.form:
        xml_data = request.form['xml']
        try:

            parser = etree.XMLParser(load_dtd=True, resolve_entities=True)
            tree = etree.fromstring(xml_data.encode(), parser)
            output = f"Parsed XML: {etree.tostring(tree, encoding='unicode')}"
        except Exception as e:
            output = f"XML Parsing Error: {e}"


    elif 'endpoint' in request.form:
        url = request.form['endpoint']
        try:

            headers = {}
            if 'headers' in request.form:
                headers = json.loads(request.form['headers'])

            data = None
            if 'data' in request.form:
                data = request.form['data']


            response = requests.post(url, headers=headers, data=data, verify=False)
            output = f"Remote response: {response.text[:200]}"
        except Exception as e:
            output = f"Request error: {e}"


    elif 'username' in request.form:
        username = request.form['username']
        try:

            query = "SELECT password FROM users WHERE username = '{}'".format(username)
            cursor.execute(query)
            result = cursor.fetchone()
            if result:
                output = f"Password for {username}: {result[0]}"
            else:
                output = "User not found."
        except Exception as e:
            output = f"SQL Error: {e}"

    return render_template('result.html', output=output, script_name=SCRIPT_NAME)


application = DispatcherMiddleware(Flask('dummy_app'), {
    '/app': app
})

if __name__ == '__main__':

    os.environ['FLASK_ENV'] = 'development'
    run_simple('0.0.0.0', 8080, application, use_reloader=True, use_debugger=True)

