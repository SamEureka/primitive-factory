import os
import subprocess
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'supersecresd7na3na8883nfa8fnasndf38tkey'
app.config['UPLOAD_FOLDER'] = '/factory/ui/static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def convert_image(filename):
    output_path = f"{app.config['UPLOAD_FOLDER']}/primitive-{filename}"
    primitive_cmd = f"/go/bin/primitive -i {filename} -o {output_path} -n 1000"
    
    try:
        subprocess.run(primitive_cmd, check=True, shell=True)
        flash('Image converted successfully')
    except subprocess.CalledProcessError:
        flash('Error occurred while converting the image')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if file was uploaded
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # Check if file name is empty
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        # Check if file is allowed
        if not allowed_file(file.filename):
            flash('Invalid file type. Allowed types are jpg, jpeg, and png')
            return redirect(request.url)

        # Save the uploaded file
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('File uploaded successfully')

        # Convert the image
        convert_image(filename)
        flash('Image converted successfully')

        return redirect(url_for('index'))

    # Retrieve all uploaded files
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    cards = []
    for file in files:
        if file.startswith('primitive-'):
            original_filename = file.split('-')[1]
            cards.append({
                'filename': original_filename,
                'image_path': url_for('static', filename=f'uploads/{file}'),
                'download_url': url_for('static', filename=f'uploads/{file}', _external=True)
            })

    return render_template('index.html', cards=cards)

@app.route('/photos')
def photos():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    cards = []
    for file in files:
        if file.startswith('primitive-'):
            original_filename = file.split('-')[1]
            cards.append({
                'filename': original_filename,
                'image_path': url_for('static', filename=f'uploads/{file}'),
                'download_url': url_for('static', filename=f'uploads/{file}', _external=True)
            })

    return render_template('photos.html', cards=cards)

if __name__ == '__main__':  # Set a secret key for flash messages
    app.run(debug=True)
