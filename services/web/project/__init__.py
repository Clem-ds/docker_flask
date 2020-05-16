import os

from sys import stderr

from werkzeug.utils import secure_filename
from flask import (
    Flask,
    jsonify,
    send_from_directory,
    request,
    redirect,
    url_for,
    render_template
)
from flask_sqlalchemy import SQLAlchemy

import sys
from os.path import abspath, dirname
sys.path.insert(0, dirname(dirname(abspath(__file__))))

#from pyfunc import testbye as tb

#import pyfunc.testbye as tb

#tb.byebye()


app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)

#pour test et règle problèmes d'import  de modules locaux
#faire python __init__.py pour lancer serveur
#mais erreurs 404 ensuite
#app.run(use_reloader=False)

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, email):
        self.email = email

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    #return jsonify(hello="world")
    data = {       
        'url_resemploigraph': url_for('static', filename = "data/resemploigraph.csv"),
        'url_recrutement_externe': url_for('static', filename = "data/recrutement_externe.csv"),
        'url_effectifparentite': url_for('static', filename = "data/effectifparentite.csv"),
        'url_departements': url_for('static', filename = "data/departements.geojson"),
        'url_effectifparregion': url_for('static', filename = "data/effectifparregion4.csv"),
        'url_donnees_insee_poleemploi': url_for('static', filename = "data/donnees_insee_poleemploi.csv")
    }
        

    print("test print", file=stderr)
    return render_template('index.html', data=data)


@app.route("/static/<path:filename>")
def staticfiles(filename):
    return send_from_directory(app.config["STATIC_FOLDER"], filename)

@app.route("/media/<path:filename>")
def mediafiles(filename):
    return send_from_directory(app.config["MEDIA_FOLDER"], filename)


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["MEDIA_FOLDER"], filename))
    return f"""
    <!doctype html>
    <title>upload new File</title>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file><input type=submit value=Upload>
    </form>
    """


@app.route('/update', methods=['GET', 'POST'])  
def update():  
    return render_template("file_upload_form.html")  



@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        print('req',request)
        f = request.files['fileinscrits']  

        print('reqform',request.form)
        print('date',request.form['startfile'])


        f.save(f.filename)  
        return render_template("success.html", name = f.filename) 

"""
#pour la phase développement
if __name__ == '__main__':  

    app.run(debug = True)   """
