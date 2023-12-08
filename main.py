from flask import Flask,render_template,flash, Blueprint,blueprints,request
from second import second
import os
from db.db import db
from camer.camera_a import camera_a
import sqlite3
app= Flask(__name__)
app.secret_key='123'
app.register_blueprint(second,url_prefix="")
app.register_blueprint(db,url_prefix="")
app.register_blueprint(camera_a,url_prefix="")
@app.route('/')
def home():
    return render_template('index.html')



con=sqlite3.connect("image.db")
con.execute("CREATE TABLE IF NOT EXISTS image(pid INTEGER PRIMARY KEY, img TEXT)")
con.close()
app.config['UPLOAD_FOLDER']="static\images"

@app.route('/upload',methods=['GET','POST'])
def upload():
    con=sqlite3.connect("image.db")
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("select * from image")
    data=cur.fetchall()
    con.close()
    if request.method=='POST':
        upload_image=request.files['upload_image']
        if upload_image.filename!='':
            filepath=os.path.join(app.config['UPLOAD_FOLDER'],upload_image.filename)
            upload_image.save(filepath)
            con=sqlite3.connect("image.db")
            cur=con.cursor()
            cur.execute("insert into image(img)values(?)",(upload_image.filename,))
            con.commit()
            flash("File upload Successfully","success")


            con=sqlite3.connect("image.db")
            con.row_factory=sqlite3.Row
            cur=con.cursor()
            cur.execute("select * from image")
            data=cur.fetchall()
            con.close()
            return render_template("upload.html",data=data)

        
    return render_template("upload.html",data=data)









if __name__=="__main__":
    app.run(debug=True)
    
