import os
from flask import Flask, render_template,request, redirect

from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(basedir, 'bd_participants.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.app_context().push()

db = SQLAlchemy(app)

class Participants(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    telephone = db.Column(db.db.Integer)
    email = db.Column(db.String(100))

    def __init__(self, nom, prenom, telephone, email):
        self.nom = nom
        self.prenom = prenom
        self.telephone = telephone
        self.email = email

@app.before_first_request
def create_tables():
    db.create_all()

def init_db():
    db.create_all()


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        nom = request.form['nom'] #on recupere le nom
        prenom = request.form['prenom'] #on recupere le prenom
        telephone = request.form['telephone'] #on recupere le numero telephone
        email = request.form['email'] #on recupere l'email
        nouveau_participant = Participants(nom = nom, prenom = prenom, telephone = telephone, email = email)
        try : 
            db.session.add(nouveau_participant)
            db.session.commit()
            return redirect("/")
        except Exception : 
            return "Une erreur s'est produite"
    
    else : 
        return render_template("home.html")
        #participants = Participants.query.all()
    #return render_template("home.html", participants = participants)

@app.route("/liste_participants/")
def liste_participants():
    participants = Participants.query.all()
    return render_template("liste_participants.html", participants = participants)

if __name__ == "__main__":
    app.run(debug = True)

