from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
import cv2
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with any random string

# Create folders if they don't exist
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
for folder in [UPLOAD_FOLDER, RESULT_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    original = None
    result = None

    if request.method == 'POST':
        method = request.form.get('method')
        file = request.files.get('image')

        # If file is uploaded, save and store in session
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            session['image_path'] = filepath
            session['filename'] = filename
            original = f'uploads/{filename}'
        else:
            # No new file uploaded; use existing session image
            filepath = session.get('image_path')
            filename = session.get('filename')
            if filepath:
                original = f'uploads/{filename}'
            else:
                return "No image uploaded yet. Please upload an image first."

        # Read the image
        img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)

        if method == 'canny':
            edges = cv2.Canny(img, 100, 200)
        elif method == 'sobel':
            sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)
            sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=5)
            edges = cv2.magnitude(sobelx, sobely)
            edges = cv2.convertScaleAbs(edges)
        elif method == 'laplacian':
            edges = cv2.Laplacian(img, cv2.CV_64F)
            edges = cv2.convertScaleAbs(edges)
        else:
            return "Invalid method selected"

        result_filename = f"{method}_{filename}"
        result_path = os.path.join(app.config['RESULT_FOLDER'], result_filename)
        cv2.imwrite(result_path, edges)
        result = f'results/{result_filename}'

        return render_template('index.html', original=original, result=result)

    return render_template('index.html', original=None, result=None)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/results/<filename>')
def result_file(filename):
    return send_from_directory(app.config['RESULT_FOLDER'], filename)

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)