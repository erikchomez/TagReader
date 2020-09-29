from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename

import processing
import os

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'UPLOAD_FOLDER')
PROCESSED_IMAGES = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'PROCESSED_IMAGES')
ALLOWED_EXTENSIONS = {'.txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_IMAGES'] = PROCESSED_IMAGES


@app.route('/')
def index():
    return render_template('index1.html')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            processing.process_image(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            return redirect(url_for('uploaded_file', filename='processed_image.jpg'))

    return redirect(url_for('index'))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)







