from flask import Flask, render_template, request, jsonify, send_file, url_for
import pyautogui
import qrcode
import io
from PIL import Image

app = Flask(__name__)

CODE_WORD = "secret"

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
    return render_template('control.html')

@app.route('/command', methods=['POST'])
def command():
    data = request.json
    if data['code_word'] != CODE_WORD:
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)