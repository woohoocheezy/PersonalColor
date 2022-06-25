from flask import Flask, render_template, request
from PIL import Image
import model

app = Flask(__name__)

@app.route('/')
def home():  # upload a photo
    return render_template('home.html')

@app.route('/result', methods = ['GET', 'POST'])
def result(): # a predicted result of the photo
    if request.method == 'POST':
        f = request.files['file']

        # model predict
        img = Image.open(f)
        predict_num = model.inference(img)

        if predict_num == 0:
            return render_template('spring.html')
        elif predict_num == 1:
            return render_template('summer.html')
        elif predict_num == 2:
            return render_template('fall.html')
        else :
            return render_template('winter.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug = True)