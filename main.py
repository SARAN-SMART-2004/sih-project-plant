from flask import Flask,render_template,flash, Blueprint,blueprints,request,redirect,url_for
from second import second
from flask_wtf import FlaskForm

from flask_bcrypt import Bcrypt
import os
import pandas as pd
from werkzeug.utils import secure_filename
from flask_pymongo import PyMongo

from datetime import datetime
app = Flask(__name__)
app.secret_key='123'
app.register_blueprint(second,url_prefix="")

# Configuration for MongoDB
app.config['MONGO_URI'] = 'mongodb://localhost:27017/image_db'
mongo = PyMongo(app)
@app.route('/login', methods=['GET', 'POST'])
def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            user_data = mongo.db.user.find_one({'username': username, 'password': password})
            if user_data:
                flash('Login successful!', 'success')
                return render_template('index.html')
            else:
                flash('Invalid username or password', 'danger')
        
        return render_template('login.html')
@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
            username = request.form.get('username', '')
            password = request.form.get('password', '')
            # You should hash and salt the password in a real-world application
            mongo.db.user.insert_one({'username': username, 'password': password})
            flash('Sign up successful! Please log in.', 'success')
            return redirect(url_for('login'))
    else:
        flash('Sign up successful! Please log in.', 'success')
    return render_template('login.html')
    








# Configuration for file upload
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
excel_file_path = 'backednd\plant dataset.xlsx'





@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            timestamp = datetime.utcnow()
            mongo.db.images.insert_one({'filename': filename, 'timestamp': timestamp})
        
            return render_template('index.html')
    return render_template('index.html')


@app.route('/display')
def display():
    #image =mongo.db.images.objects.order_by('-id').first()
    #images = mongo.db.images.find()
    import tensorflow as tf
    new_model = tf.keras.models.load_model('model_avg_20_inception.h5')
    lables = ['Aloevera',
    'Amla',
     'Amruthaballi',
     'Arali',
     'Astma_weed',
     'Badipala',
     'Balloon_Vine',
     'Bamboo',
     'Beans',
    'Betel',
     'Bhrami',
     'Bringaraja',
     'Caricature',
     'Castor',
     'Catharanthus',
     'Chakte',
     'Chilly',
     'Citron lime (herelikai)',
     'Coffee',
     'Common rue(naagdalli)',
     'Coriender',
     'Curry',
     'Doddpathre',
     'Drumstick',
     'Ekka',
     'Eucalyptus',
     'Ganigale',
     'Ganike',
    'Gasagase',
     'Ginger',
    'Globe Amarnath',
    'Guava',
    'Henna',
     'Hibiscus',
     'Honge',
    'Insulin',
     'Jackfruit',
     'Jasmine',
     'Kambajala',
     'Kasambruga',
    'Kohlrabi',
    'Lantana',
    'Lemon',
     'Lemongrass',
     'Malabar_Nut',
     'Malabar_Spinach',
     'Mango',
     'Marigold',
     'Mint',
        'Neem',
    'Nelavembu',
     'Nerale',
     'Nooni',
    'Onion',
    'Padri',
    'Palak(Spinach)',
    'Papaya',
    'Parijatha',
    'Pea',
    'Pepper',
    'Pomoegranate',
    'Pumpkin',
    'Raddish',
    'Rose',
    'Sampige',
        'Sapota',
    'Seethaashoka',
    'Seethapala',
    'Spinach1',
    'Tamarind',
    'Taro',
    'Tecoma',
    'Thumbe',
    'Tomato',
    'Tulsi',
    'Turmeric',
    'ashoka',
    'camphor',
    'kamakasturi',
    'kepala']
    # predict with new images
    import numpy as np

    
    # Get the last uploaded image from MongoDB
    
    latest_image = list(mongo.db.images.find())[-1]
    print(latest_image)
    filename = latest_image['filename']
    img = tf.keras.preprocessing.image.load_img('static/uploads/'+filename, target_size=(299, 299))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create a batch
    predictions = new_model.predict(img_array)

    score = tf.nn.sigmoid(predictions[0])
    # Read data from the Excel file
    print(np.argmax(score))
    print(filename)
    if filename:
        #filename = latest_image['filename']
        latest_image = mongo.db.images.find_one(sort=[('upload_time', 1)])
        return render_template('display.html', filename=filename,resu=lables[np.argmax(score)])
    else:
        return 'No images found in the database'
    
    #return render_template('display.html')

  

@app.route('/profile')
def profile():
    return render_template("profile.html")
@app.route('/camera', methods=['GET', 'POST'])
def camera():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            timestamp = datetime.utcnow()
            mongo.db.images.insert_one({'filename': filename, 'timestamp': timestamp})
        
            return render_template('index.html')

    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)