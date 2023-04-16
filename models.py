from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import base64


db = SQLAlchemy()


class Sublease(db.Model):
    id = db.Column(db.String(40), primary_key=True)
    subleaser_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    apartment_name = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
    rent = db.Column(db.Integer, nullable=False)
    bed = db.Column(db.Integer, nullable=True)
    bath = db.Column(db.Integer, nullable=True)
    sqft = db.Column(db.Double, nullable=True)
    location = db.Column(db.String(20), nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image_path = db.Column(db.String(255), nullable=False)


    def to_dict(self):

        with open(self.image_path, 'rb') as f:
            image_data = f.read()

        return {
            'id': self.id,
            'subleaser_id': self.subleaser_id,
            'apartment_name': self.apartment_name,
            'description': self.description,
            'rent': self.rent,
            'bed': self.bed,
            'bath': self.bath,
            'sqft': self.sqft,
            'location': self.location,
            'date_posted': self.date_posted,
            'image':base64.b64encode(image_data).decode('utf-8')
        }

class Apartment(db.Model):
    name = db.Column(db.String(40) , nullable= False, primary_key=True)
    pets = db.Column(db.Boolean, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    link = db.Column(db.String(50), nullable=False)
    pool = db.Column(db.Boolean , nullable= True)
    gym = db.Column(db.Boolean , nullable= True)
    incldUtilities = db.Column(db.Boolean , nullable=True )
    shuttleRte = db.Column(db.Boolean , nullable=True )
    indvLeasing = db.Column(db.Boolean , nullable=True )
    wsherDryer = db.Column(db.Boolean , nullable= True)
    furnished = db.Column(db.Boolean , nullable=True)
    rmMatching = db.Column(db.Boolean , nullable=True )


    def to_dict(self):
        return {
            'name': self.name,
            'pets': self.pets,
            'pool': self.pool,
            'gym': self.gym,
            'incldUtilities': self.incldUtilities,
            'shuttleRte': self.shuttleRte,
            'indvLeasing': self.indvLeasing,
            'wsherDryer': self.wsherDryer,
            'furnished': self.furnished,
            'rmMatching': self.rmMatching,
            'rating': self.rating,
            'phone': self.phone,
            'link': self.link
        }

class User(db.Model):
    id = db.Column(db.String(40), primary_key=True)
    email = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'password': self.password
        }

class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id,
            'datetime': self.datetime
        }