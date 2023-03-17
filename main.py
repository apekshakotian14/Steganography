import os
from numpy.core.arrayprint import printoptions
from PIL import Image
import pandas as pd
import numpy as np
from ImageSteg import ImageSteg
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

img = ImageSteg()

app = Flask(__name__)


# code for home.html
@app.route("/")
def home():
    return render_template("home.html")


# code for login.html
@app.route("/login")
def login():
    return render_template("login.html")


# code for upload.html
@app.route("/upload")
def submit():
    return render_template("upload.html")


# code for uploader.html
@app.route('/uploader', methods=['POST'])
def success():
    message = request.form.get("hide_message")
    start_bit = int(request.form['startbit'])
    length = int(request.form['length'])
    print(start_bit)
    print(length)
    mode = request.form['mode']
    print("message " + message)
    print("mode " + mode)
    if request.method == 'POST':
        f = request.files['file']
        # Reading the source file
        src = f.filename;
        # Reading the destination file
        dest = "stegano.png"
        f.save("static/" + src)
        # Renaming the source and destination file
        os.rename("static/" + src, "static/" + dest)
        # Encrypting the message M in carrier P
        img.encrypting_text_in_image("static/" + dest, message, "")
        # Decrypting the message M from carrier P
        decryptPath = "static/" + dest.split(".")[0] + "_encrypted.png"
        print(decryptPath)
        res = img.decrypting_text_in_image(decryptPath)
        print("Encryption Done")
        print("Decrypted message = " + res)
        return render_template("home.html", name=dest)


if __name__ == "__main__":
    app.run(debug=True)
