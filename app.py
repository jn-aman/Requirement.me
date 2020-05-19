import os
from flask import Flask, flash, request, redirect, url_for,render_template, send_file
from werkzeug.utils import secure_filename
from flask import send_from_directory
import subprocess
from flask_toastr import Toastr
import shutil
UPLOAD_FOLDER = '/Users/amanjain/Desktop/amanp/'
ALLOWED_EXTENSIONS = {'py', 'ipynb'}

app = Flask(__name__)

app.secret_key = "super secret key"
app.config['UPLOAD_FOLDER'] = app.root_path
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
toastr = Toastr(app)
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path,"static"),'logos.svg', mimetype='image/vnd.microsoft.icon')


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file present', 'error')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file','error')
            return redirect(request.url)
        if file and allowed_file(file.filename):
#            flash("Generating requirement.txt", 'info')

            filename = secure_filename(file.filename)
            foldername=filename.split(".")[0]
            try:
                os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'],foldername))
            except:
                if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'],foldername,"requirements.txt")):
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'],foldername,"requirements.txt")
                    os.remove(file_path)
                if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'],foldername,filename)):
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'],foldername,filename)
                    os.remove(file_path)
                os.rmdir(os.path.join(app.config['UPLOAD_FOLDER'],foldername))
                os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'],foldername))

            file.save(os.path.join(app.config['UPLOAD_FOLDER'],foldername,filename))
            return redirect(url_for('uploaded_file',foldername=foldername,filename=filename))
        if file and not allowed_file(file.filename):
            flash("Wrong file format", 'error')
            return redirect(request.url)
    return  render_template('index.html')

@app.route('/uploads/<foldername>/<filename>')
def uploaded_file(foldername,filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'],foldername,"requirements.txt")
    folder_path = os.path.join(app.config['UPLOAD_FOLDER'],foldername)
    print(file_path,folder_path)

    subprocess.Popen(['yes | pigar', "-p" ,file_path, '-P',folder_path], shell=True,cwd=folder_path).wait()
#    flash("Done", 'success')

    def generate():
        with open(file_path) as f:
            yield from f

        shutil.rmtree(folder_path)
    r = app.response_class(generate())
    r.headers.set('Content-Disposition', 'attachment', filename='requirements.txt')
    return r

if __name__ == "__main__": 
        app.run() 
