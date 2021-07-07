import cv2
from flask import Flask, request, send_file, render_template
from src.steganography import hideData, showData

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/encrypt.html')
def encryption():
    return render_template('encrypt.html')


@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.form.get('data')
    file = request.files['file']
    file.save('static/uploads/image1.png')
    image = cv2.imread('static/uploads/image1.png')
    encoded_image = hideData(image, data)
    cv2.imwrite('static/uploads/result.png', encoded_image)
    path = 'static/uploads/result.png'
    return send_file(path, as_attachment=True, attachment_filename='Encrypted.png', mimetype='image/png')


@app.route('/decrypt.html')
def decryption():
    return render_template('decrypt.html')


@app.route('/decrypt', methods=['POST'])
def decrypt():
    file = request.files['file']
    file.save('static/uploads/image2.png')
    image = cv2.imread('static/uploads/image2.png')
    result = showData(image)
    path = 'static/uploads/message.txt'
    textfile = open(path, 'w')
    textfile.write(result)
    textfile.close()
    return send_file(path, as_attachment=True, attachment_filename='Message.txt', mimetype='text/plain')


if __name__ == "__main__":
    app.run(debug=True)
