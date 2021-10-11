from flask import Flask, render_template, request, json, redirect
import random
import string


app = Flask(__name__)
token = "abai"


def gene_random_str():
    str_list = random.sample(string.digits + string.ascii_letters, 8)
    random_str = ''.join(str_list)

    return random_str


@app.route('/')
@app.route('/hello')
def hello():
    with open("data.json", "rb") as f:
        data = json.loads(f.read().decode("utf-8"))
    return render_template('index.html', data=data['data'])


@app.route('/details')
def details():
    with open("data.json", "rb") as f:
        data = json.loads(f.read().decode("utf-8"))
    return render_template('details.html', data=data['data'])


@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/save/', methods=['GET', 'POST'])
def save():
    img_token = request.form.get('token')
    if img_token == token:
        #  获取图片信息
        img_id = gene_random_str()
        img_data = request.files['image']
        img_name = request.form.get('name')
        img_words = request.form.get('words')

        #  存储图片至 petimg 文件夹
        tem = img_data.filename.split(".")
        path = "static/img/petimg/"
        file_path = path + img_id + "." + tem[1]
        img_data.save(file_path)

        dic = {
            "img_id": img_id,
            "img_name": img_name,
            "img_words": img_words,
            "img_url": file_path
        }
        #  读取data.json中的数据
        with open("data.json", "rb") as f:
            data = json.loads(f.read().decode("utf-8"))
            data['data'].append(dic)
        #  将数据插入data.json
        with open("data.json", "wb") as f:
            f.write(json.dumps(data).encode("utf-8"))

        return redirect('/hello')
    else:
        return "兄弟你密码是错的"


if __name__ == "__main__":
    app.run(debug=True)
