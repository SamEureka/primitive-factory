from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Set the upload directory
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Render the main page with two buttons
@app.route('/')
def index():
    return render_template('index.html')

# Handle photo upload
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist('photos')
        for file in files:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return redirect(url_for('index'))
    return render_template('upload.html')

# Serve uploaded photos
@app.route('/photos')
def photos():
    photo_files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('photos.html', photo_files=photo_files)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)