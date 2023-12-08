from flask import Flask,render_template,flash, Blueprint

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

img = tf.keras.preprocessing.image.load_img('static\images\hui.jpg', target_size=(299, 299))
img_array = tf.keras.preprocessing.image.img_to_array(img)
img_array = tf.expand_dims(img_array, 0)  # Create a batch
predictions = new_model.predict(img_array)
score = tf.nn.sigmoid(predictions[0])
#print(np.argmax(score))
#resu=print("This image most likely belongs to {} with a {:.2f} percent confidence.".format(lables[np.argmax(score)], 100 * np.max(score)))



second=Blueprint("second", __name__,static_folder="static",template_folder="templates")
@second.route('/s')
def s():
    return render_template("s.html")

@second.route('/result')
def result():
    return render_template('result.html',resu=lables[np.argmax(score)])
