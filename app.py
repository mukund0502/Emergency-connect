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
        phone = request.form.get('phone')
        password1 = request.form.get('password1')
        aadhar = request.form.get('aadhar')
        pan = request.form.get('pan')
        address = request.form.get('address')
        
        cur = db.connection.cursor()
        cur.execute("insert into adminn values(%s,%s,%s, %s, %s, %s, %s, %s )", (fname, lname, phone, email, aadhar, pan, password1, address))
        # cur.execute("INSERT INTO USER values (%s, %s, %s, %s, %s)", (uname, fname, lname, email, password1))
        db.connection.commit()

        return redirect(url_for('home'))
    return render_template('login.html')


@app.route('/delete/<int:id>')
def delete(id):
    sql_query = "delete from calamity where contact_no = %s"
    print(id)
    values = (str(id))
    print(type(values))
    cur = db.connection.cursor()
    cur.execute(sql_query, [values])
    print(sql_query, values)
    db.connection.commit()
    # return render_template('showcalamity.html')
    return redirect(url_for('showcalamity'))


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
        # sendmail()
        print('done')
        return render_template('updatedb.html')
    return render_template('updatedb.html')



def fetchdetails():
    cur = db.connection.cursor()
    abc = "select * from calamity"
    rr = cur.execute(abc)
    detail = cur.fetchall()
    cur.close()
    # print(detail)
    return detail

def sendmail(name, contactno, address, calamity):
    import smtplib
    server = smtplib.SMTP('smtp.googlemail.com', 587)
    server.starttls()
    server.login('rajeevranjanjop@gmail.com', 'FirstJobapply@17')
    body = name+" "+contactno+" " +address+" "+calamity+"."
    server.sendmail('rajeevranjanjop@gmail.com', 'mukundwh8@gmail.com', body)
    print('sent')


if __name__ == '__main__':
    app.run(debug=True)
