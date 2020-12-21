from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

from pages.process import hitung, hapus

app = Flask(__name__)
CORS(app)

@app.route('/home')
@app.route('/', methods=['GET'])
def home():
    return render_template('uploader.html')


@app.route('/uploader', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        perbesaran = request.form['perbesaran']
        filename = f.filename
        f.save('static/temp/' + filename)
        files = filename
        return hitung(files, perbesaran)
    else:
        return "<h1>404 NOT FOUND</h1>"


@app.route('/deletegambar', methods=['POST'])
def deleteGambar():
    filename = request.form['filename']
    hapus(filename)
    return jsonify(
        status="success",
        msg="Sukses Menghapus Data"
    )


app.run()
