from flask import Flask,render_template,flash, Blueprint,blueprints,request,redirect,url_for
#from second import second
import os
from werkzeug.utils import secure_filename
#from camer.camera_a import camera_a
from flask_pymongo import PyMongo
app = Flask(__name__)

# Configuration for MongoDB
app.config['MONGO_URI'] = 'mongodb://localhost:27017/image_db'
mongo = PyMongo(app)

# Configuration for file upload
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            mongo.db.images.insert_one({'filename': filename})
            return redirect(url_for('index'))
    return render_template('upload.html')

@app.route('/display')
def display():
    images = mongo.db.images.find()
    return render_template('display.html', images=images)



if __name__ == '__main__':
    app.run(debug=True)