## postgres database stuffie
import os 
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

## eg code, get the actual connection string from vercel 


db=SQLAlchemy(app)

class Classroom(db.Model):
   id=db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
   class_name = db.Column(db.String(100), nullable=False)
   description = db.Column(db.String(1000), unique=True, nullable=False)
   rating = db.Column(db.Integer)
   numOfRatings = db.Column(db.Integer)

   # teacher name 
   def __repr__(self):
       return f"<id: {self.id} class_name: {self.class_name}, description: {self.description}, rating: {self.rating}, numOfRatings: {self.numOfRatings})>"

@app.route('/test')
def test():
    return 'hello World';

@app.route('/')
def index():
    classes = Classroom.query.all()
    print(classes)
    return render_template('./index.html', classes=classes)


@app.route('/addrating', methods=['POST'])
def add_rating():
   print(request.json)
   rating = request.json['rating']
   class_id=request.json['class_id']
   if rating == None or class_id == None: 
       return "No 'rating' or 'class_id'", 400
   
   classroom = Classroom.query.filter_by(id=class_id).first()

   if classroom == None:
       return f"None such class '{class_id}'", 400
   num_current_ratings = classroom.numOfRatings
   
   # have some variable new_rating that contains the updated rating
   # update classroom.rating = new_rating
   # increment numOfRatings
   
   classroom.rating = (rating + classroom.rating) / num_current_ratings
   classroom.numOfRatings += 1;
   
   db.session.add(classroom)
   db.session.commit()
   return "done", 200

