import os
from flask import Flask, request, redirect, render_template, flash, session
from werkzeug.utils import secure_filename
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.preprocessing import image

import numpy as np


classes = ["線状の","粒々の","もくもくとした","ふわっとした","", ""]
image_size = 200

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

model = load_model('./model.h5')#学習済みモデルをロード


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template("test-index.html",answer='ファイルがありません')
        file = request.files['file']
        if file.filename == '':
            return render_template("test-index.html",answer='ファイルがありません')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            filepath = os.path.join(UPLOAD_FOLDER, filename)

            #受け取った画像を読み込み、np形式に変換
            img = image.load_img(filepath,  target_size=(image_size,image_size,3))
            img = image.img_to_array(img)
            data = np.array([img])
            
            #変換したデータをモデルに渡して予測する
            result = model.predict(data)[0]
            predicted = result.argmax()
            ans_per = float(result[predicted]*100)

            pred_answer = "これは 【 " + classes[predicted] + "雲 】 です"
  
        return render_template("test-index.html",answer=pred_answer)

    return render_template("test-index.html",answer="")


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host ='0.0.0.0',port = port)