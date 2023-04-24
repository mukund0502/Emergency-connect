from flask import Flask, render_template, request ,redirect, url_for
from flask_mysqldb import MySQL
import yaml
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)

with open("db.yaml") as f:
    db = yaml.full_load(f) 
app.config['MYSQL_HOST'] = db['mqsql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

db = MySQL(app)

@app.route('/', methods = ['POST', 'GET'])
def home():
    return render_template('index.html')

@app.route('/services', methods = ['POST', 'GET'])
def services():
    return render_template('services.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST' :
        email = request.form.get('email')
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        uname = request.form.get('uname')
        phone = request.form.get('phone')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        if(email=='' or fname=='' or lname =='' or uname =='' or len(password1)<8):
            info = "*every space is required and password length should greater than 7."
            return render_template('signup.html', info = info)
        elif(password1!=password2):
            info = "*password doesn't match!"
            return render_template('signup.html', info = info)
        
        cur = db.connection.cursor()
        ret = cur.execute("select * from user where email=%s or uname = %s", (email, uname))
        if(ret>0):
            info = "*Account already exist!"
            return render_template('signup.html', info = info)


        cur = db.connection.cursor()
        # print(uname, fname, lname, email, password1)
        cur.execute("INSERT INTO USER values (%s, %s, %s, %s, %s)", (uname, fname, lname, email, password1))
        db.connection.commit()

        return redirect(url_for('/login', uname = uname))
    return render_template('login.html')

@app.route('/about', methods = ['POST', 'GET'])
def about():
    return render_template('about.html')

@app.route('/contact', methods = ['POST', 'GET'])
def contact():
    return render_template('contact.html')

@app.route('/live_maps', methods = ['POST', 'GET'])
def live_maps():
    return render_template('live_maps.html')



@app.route('/showcalamity', methods = ['POST', 'GET'])
def showcalamity():
    person = fetchdetails()
    return render_template('showcalamity.html', person = person)



@app.route('/updatedb', methods = ['POST', 'GET'])
def updatedb():
    if request.method =='POST':
        name = request.form['name']
        address = request.form['address']
        contact = request.form['contact']
        calamity = request.form['calamity']
        sql_query = "INSERT INTO calamity (name, address, contact_no, calamity) VALUES (%s, %s, %s, %s)"
        values = (name, address, contact, calamity)
        cur = db.connection.cursor()
        cur.execute(sql_query, values)
        db.connection.commit()
        return render_template('updatedb.html')
    return render_template('updatedb.html')



def fetchdetails():
    cur = db.connection.cursor()
    abc = "select * from calamity"
    rr = cur.execute(abc)
    detail = cur.fetchall()
    cur.close()
    print(detail)
    return detail


if __name__ == '__main__':
    app.run(debug=True)
