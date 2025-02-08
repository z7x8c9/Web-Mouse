from flask import Flask, render_template, request, jsonify, send_file, url_for, session, redirect, make_response
import pyautogui
import qrcode
import io
from PIL import Image
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  

def get_code_word():
    with open('code.json', 'r') as file:
        data = json.load(file)
    return data['code_word']

def set_code_word(new_code_word):
    with open('code.json', 'w') as file:
        json.dump({"code_word": new_code_word}, file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/qr')
def qr():
    img = qrcode.make('http://192.168.0.101:5000/control')
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

@app.route('/control')
def control():
    code_word_cookie = request.cookies.get('code_word')
    if code_word_cookie == get_code_word():
        return render_template('control.html')
    else:
        return redirect('/login?next=control')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        code_word = request.form['code_word']
        if code_word == get_code_word():
            resp = make_response(redirect(request.args.get('next') or '/control'))
            resp.set_cookie('code_word', code_word)
            return resp
        else:
            return render_template('login.html', error='Incorrect code word')
    return render_template('login.html')

@app.route('/verify_code_word', methods=['POST'])
def verify_code_word():
    data = request.json
    if data['code_word'] == get_code_word():
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error'}), 403

@app.route('/command', methods=['POST'])
def command():
    data = request.json
    code_word_cookie = request.cookies.get('code_word')
    if code_word_cookie != get_code_word() or data['code_word'] != get_code_word():
        return jsonify({'status': 'error', 'message': 'Incorrect code word'}), 403

    action = data['action']
    if action == 'left_click':
        pyautogui.click()
    elif action == 'right_click':
        pyautogui.rightClick()
    elif action == 'scroll':
        pyautogui.scroll(data['value'])
    elif action == 'move':
        pyautogui.move(data['x'], data['y'])

    return jsonify({'status': 'success'})

@app.route('/update_code_word', methods=['POST'])
def update_code_word():
    new_code_word = request.form['new_code_word']
    set_code_word(new_code_word)
    return jsonify({'status': 'success', 'message': 'Code word updated'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
