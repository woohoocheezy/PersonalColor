from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16MB 제한

app = Flask(__name__)

@app.route('/')
def home():  # upload a photo
    return render_template('home.html')

@app.route('/result', methods = ['GET', 'POST'])
def result(): # a predicted result of the photo
    if request.method == 'POST':
        f = request.files['file']
        f.save('./uploads/' + secure_filename(f.filename))

        # model predict
        predict_num = 1

        if predict_num == 0:
            return render_template('result.html')
        elif predict_num == 1:
            return render_template('result1.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug = True)