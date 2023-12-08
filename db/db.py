from flask import Flask, render_template,request,flash,redirect,url_for,Blueprint
import sqlite3
db=Blueprint("db", __name__,static_folder="static",template_folder="templates")
con=sqlite3.connect("database.db")
con.execute("CREATE TABLE IF NOT EXISTS data(pid INTEGER PRIMARY KEY, name TEXT,address TEXT)")
con.close()

@db.route('/ds')
def s():
    return render_template("ds.html")
