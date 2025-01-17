import os
from flask import Flask, request, redirect, render_template, flash, session, jsonify
from werkzeug.utils import secure_filename
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.preprocessing import image

import numpy as np

classes = ["線状の","粒々の","もくもくとした","ふわっとした","うろこ状の", "霧状の"]
pokes = ["ピッピ", "ドータクン", "カラサリス", "トラパルト", "ヨワシ", "マッスグマ"]

image_size = 200
image_resize = 300

UPLOAD_FOLDER = "static"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

#app = Flask(__name__, static_folder="./uploads/")
app = Flask(__name__, static_folder="./static/")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

model = load_model('./model.h5')#学習済みモデルをロード
model_poke = load_model('./model_poke15.h5')

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
            
            img_resized = image.load_img(filepath, target_size=(image_resize,image_resize,3))
            img_resized = image.img_to_array(img_resized)
            data_poke = np.array([img_resized])
            
            
            #変換したデータをモデルに渡して予測する
            result = model.predict(data)[0]
            result_poke= model_poke.predict(data_poke)[0]
            predicted = result.argmax()#正解クラス
            predicted_poke = result_poke.argmax()
            accuracy_percentage = result[predicted] * 1# 正解クラスに対する確率
            accuracy_percentage_poke = result_poke[predicted_poke]*1
            ans_per = float(result[predicted])
            ans_per_poke = float(result_poke[predicted_poke])

            pred_answer = (
            #f"これは 【  {classes[predicted]}雲 】 です"
            #"適合率は{accuracy_percentage:.2f}%です"
            #f"一番似ているポケモンは 【{pokes[predicted_poke]} 】です"
            #"適合率は{accuracy_percentage_poke:.2f}%です"
            #f"カレントディレクトリは 【{os.getcwd()} 】です"
            )
            poke_image ="./static/images/"+f"{pokes[predicted_poke]}.png"
            #どのポケモンか、デフォルト値も設定
            poke_answer = pokes[predicted_poke] if predicted_poke < len(pokes) else "不明なポケモン"
            print(classes[predicted])
            print(poke_answer)
            print(poke_image)
            
        return jsonify({'cloud_answer': classes[predicted], 'poke_answer': poke_answer, 'image_path': poke_image})
        #return render_template("test-index.html",cloud_answer="佐藤",poke_answer=poke_answer, image_path=poke_image)

    return render_template("test-index.html",answer="")

@app.route('/static/<filename>')
def uploaded_file(filename):
    os.path.abspath(UPLOAD_FOLDER + filename)
    return render_template("test-index.html", img="uploadss" + filename + ".png")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host ='0.0.0.0',port = port)