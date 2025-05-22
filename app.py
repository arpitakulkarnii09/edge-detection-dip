from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
import os
import cv2
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  

UPLOAD_FOLDER = 'static/uploads/'
RESULT_FOLDER = 'static/results/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    original = result = None

    if request.method == 'POST':
        method = request.form.get('method')
        uploaded_file = request.files.get('image')

       
        if uploaded_file:
            filename = secure_filename(uploaded_file.filename)
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            uploaded_file.save(image_path)
            session['image_path'] = image_path
        else:
            image_path = session.get('image_path')

        if image_path and method:
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

            if method == 'canny':
                edges = cv2.Canny(img, 100, 200)
            elif method == 'sobel':
                edges = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)
            elif method == 'laplacian':
                edges = cv2.Laplacian(img, cv2.CV_64F)

            result_filename = f"{method}_{os.path.basename(image_path)}"
            result_path = os.path.join(RESULT_FOLDER, result_filename)
            cv2.imwrite(result_path, edges)

            original = image_path
            result = result_path

    return render_template('index.html', original=original, result=result)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/results/<filename>')
def result_file(filename):
    return send_from_directory(RESULT_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)