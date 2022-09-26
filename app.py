#!/usr/bin/env python3
from wsgiref.util import request_uri
from flask import Flask, render_template, url_for, request, redirect, session, flash, send_file
from flask_mysqldb import MySQL
import qrcode
import os
import glob
import cv2
from PIL import Image
import io

CAR_FOLDER = os.path.abspath("C:/Users/Park Yu Min/Desktop/flaskDemo/static/cars")

app= Flask(__name__)
app.secret_key = "super secret key"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'users'

app.config['UPLOAD_FOLDER'] = CAR_FOLDER

mysql = MySQL(app)

@app.route('/')
def cars():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM car")
    data = cursor.fetchall()

    car_name = 'Tacoma'+'.jpg'
    
    file_name = os.path.join(app.config['UPLOAD_FOLDER'], car_name)
    print(file_name)
    return render_template("cars.html", value=data, car_image=file_name)

    

#---------- car details ------------------------------------------------------------
@app.route('/car_details/<id>', methods=['GET', 'POST'])
def car_details(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM car WHERE id=%s", str(id))
    data = cursor.fetchall()     

    for c in data:
        name = str(c[2])+'.jpg'



    file_name = os.path.join(app.config['UPLOAD_FOLDER'], name)
    print(file_name)
    if request.method=='POST':

        # Encoding data using make() function
        img = qrcode.make()
        # Creating an instance of QRCode class
        qr = qrcode.QRCode(version = 1, box_size = 10, border = 5)
        # Save the specific data into the qr \
        count = id
        dat = "CSIT321 : " + str(count) 
        qr.add_data(dat)

        # making the QR image
        qr.make(fit = True)
        img = qr.make_image()
        buf = io.BytesIO() # Generate a new buffer bytes object
        img.save(buf)
        buf.seek(0)
        return send_file(buf,mimetype='image/jpeg')
        #img.save('static/qrcode/'+str(count)+'.jpg')

    return render_template("car_details.html", value=data, id=id, name=name,car_image=file_name)


if __name__ == '__main__':
    #app.run(debug = True)
    app.run(debug=True)