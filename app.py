from flask import Flask, request, jsonify
from secret.Keys import appkey 
from models import User, Messages, Sublease, Apartment, db
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import uuid
import os
import base64
from flask_cors import CORS
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()




app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'iwgrupwG478IUWGFPW7G23G7FPAS9FG7' #I know it's bad practice but
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['UPLOAD_FOLDER'] = 'images'


db.init_app(app)
with app.app_context():
    db.create_all()

#test this server by running 'python routes.py in terminal, then curling in a different terminal
#install a vscode extension to view database

#returns JSON for a specific account given their ID
#test with curl 127.0.0.1:5000/account/0
@app.route('/account/<string:id>', methods=['GET'])
def getUser(id):
  user = User.query.get(id) #TODO update this to UUID and in database as well
  if not user:
        return jsonify({'error': 'User not found'}), 404
  user_dict = user.__dict__
  del user_dict['_sa_instance_state']
  return jsonify(user_dict)
@app.route('/')
def testdata():
    return {'yay': 'it worked!'}

#add a user to database, returns json from user in database
#test with curl --location --request POST '127.0.0.1:5000/signup' --header 'Content-Type: application/x-www-form-urlencoded' --data-urlencode 'username=johndoe' --data-urlencode 'password=secret' --data-urlencode 'email=john@doe.com' --data-urlencode 'id=0'
#CONNECTED TO REACT
@app.route('/api/signup', methods=['POST'])
def addUser():
    id = request.json['userId']
    email = request.json['email']
    password = request.json['password']
    username = request.json['username']

    print(f'\nNew User: {request.json} recieved')

    newUser = User(id=id, name=username, email=email, password=generate_password_hash(password, method='sha256'))
    db.session.add(newUser)
    db.session.commit()
    return getUser(id) ##return json of new user to confirm it worked

#add a listing to database, returns object from listing in database
#test with curl --location --request POST '127.0.0.1:5000/addListing' --header 'Content-Type: application/x-www-form-urlencoded' --data-urlencode 'apartment=' --data-urlencode 'rent=1000' --data-urlencode 'user_id=1' --data-urlencode 'bed=4' --data-urlencode 'bath=3' --data-urlencode 'sqft=2000' --data-urlencode 'location=houston' --data-urlencode 'description=This beautiful house is perfect for families or groups. It features three bedrooms, two bathrooms, a large living room, and a fully equipped kitchen. The house is located in a quiet, tree-lined neighborhood with easy access to shopping and dining.'
@app.route('/api/listings', methods=['POST'])
def addSublet():
    print(request)
    id = str(uuid.uuid4())
    subleaser_id = request.form['user_id']
    apartment_name = request.form['apartment']
    rent = request.form['rent']
    bed = request.form['bed']
    bath = request.form['bath']
    sqft = request.form['sqft']
    desc = request.form['description']
    location = request.form['location']
    image_file = request.files['image']
    image_filename = secure_filename(image_file.filename)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
    image_file.save(image_path)

    newListing = Sublease(id=id, subleaser_id=subleaser_id, apartment_name=apartment_name, rent=rent, bed=bed, bath=bath, sqft=sqft, description=desc, location=location, image_path=image_path)
    db.session.add(newListing)
    db.session.commit()

    return jsonify(newListing.to_dict()) #TODO change this to JSON once getListing route implemented


#gets a listing by id, and deletes it if that's the request method
@app.route('/api/listings/<string:listing_id>', methods=['GET', 'DELETE'])
def manage_listing(listing_id):
    listing = Sublease.query.get_or_404(listing_id)

    


    if request.method == 'DELETE':
        os.remove(listing.image_path) # remove image file from file system
        db.session.delete(listing)
        db.session.commit()
        return '', 204  # Return empty response with 204 status code for successful deletion
    elif request.method == 'GET':
        return jsonify(listing.to_dict())

#gets a list of json representations of all listings with param arguments to filter
#test with curl 127.0.0.1:5000/api/sublets
#CONNECTED TO REACT
@app.route('/api/sublets', methods=['GET'])
def get_sublets():
    print("hello")
    min_price = request.args.get('min_price', '')
    max_price = request.args.get('max_price', '')
    max_beds = request.args.get('max_beds', '')
    min_beds = request.args.get('min_beds', '')
    max_baths = request.args.get('max_baths', '')
    min_baths = request.args.get('min_baths', '')
    max_sqft = request.args.get('max_sqft', '')
    min_sqft = request.args.get('min_sqft', '')
    before = request.args.get('before', '')
    after = request.args.get('after','')
    apartment = request.args.get('apartment', '')
    location = request.args.get('location', '')
    user = request.args.get('user','')
    sort_by = request.args.get('sort_by', '')


    sublets = Sublease.query
    if max_price:
        sublets = sublets.filter(Sublease.rent <= max_price)
    if max_baths:
        sublets = sublets.filter(Sublease.rent <= max_baths)
    if max_beds:
        sublets = sublets.filter(Sublease.bed <= max_beds)
    if max_sqft:
        sublets = sublets.filter(Sublease.sqft <= max_sqft)
    if min_baths:
        sublets = sublets.filter(Sublease.bath >= min_baths)
    if min_beds:
        sublets = sublets.filter(Sublease.bed >= min_beds)
    if min_sqft:
        sublets = sublets.filter(Sublease.sqft >= min_sqft)
    if min_price:
        sublets = sublets.filter(Sublease.rent >= min_price)
    if before: 
        sublets = sublets.filter(Sublease.date_posted <= before)
    if after: 
        sublets = sublets.filter(Sublease.date_posted >= after)
    if location:
        sublets = sublets.filter(Sublease.location == location)
    if apartment:
        sublets = sublets.filter(Sublease.apartment_name == apartment)
    if user:
        sublets = sublets.filter(Sublease.subleaser_id == user)
        
    # Sort the Sublease objects based on the query parameter
    if sort_by == 'price_inc':
        sublets = sublets.order_by(Sublease.rent.asc())
    elif sort_by == 'price_dec':
        sublets = sublets.order_by(Sublease.rent.desc())
    elif sort_by == 'sqft_inc':
        sublets = sublets.order_by(Sublease.sqft.asc())
    elif sort_by == 'sqft_dec':
        sublets = sublets.order_by(Sublease.sqft.desc())
    elif sort_by == 'beds_inc':
        sublets = sublets.order_by(Sublease.bed.asc())
    elif sort_by == 'beds_dec':
        sublets = sublets.order_by(Sublease.bed.desc())
    elif sort_by == 'baths_inc':
        sublets = sublets.order_by(Sublease.bath.asc())
    elif sort_by == 'baths_dec':
        sublets = sublets.order_by(Sublease.bath.desc())
    elif sort_by == 'date_inc':
        sublets = sublets.order_by(Sublease.date_posted.asc()) 
    elif sort_by == 'date_dec': #I just realized this could've just been one condition and dictionary .....
        sublets = sublets.order_by(Sublease.date_posted.desc())  #I'll fix it eventually ... (No I won't)

    sublets_list = [sublet.to_dict() for sublet in sublets]
    return jsonify(sublets_list)


'''
###################
ROUTES FOR MESSAGES
###################
'''

#TODO add message

#TODO get message from id

#TODO get messages from user, sort and filter, should be easy to get conversation

#TODO delete message, might not need route unless we want to let users delete them


'''
###################
ROUTES FOR APARTMENTS
###################
'''

#add apartment, might not need to be route
@app.route('/api/apartments', methods=['POST'])
def addApartment():
    name = request.json['name']
    pets = request.json['pets']
    pool = request.json['pool']
    gym = request.json['gym']
    incldUtilities = request.json['incldUtilities']
    shuttleRte = request.json['shuttleRte']
    indvLeasing = request.json['indvLeasing']
    wsherDryer = request.json['wsherDryer']
    furnished = request.json['furnished']
    rmMatching = request.json['rmMatching']


    newApartment = Apartment(name=name, pets=pets, pool=pool, gym=gym, incldUtilities=incldUtilities, shuttleRte=shuttleRte, indvLeasing=indvLeasing, wsherDryer=wsherDryer, furnished=furnished, rmMatching=rmMatching)
    db.session.add(newApartment)
    db.session.commit()

    return jsonify(newApartment.to_dict())

#TODO get apartment from id

#TODO get apartments with sort and filter
@app.route('/api/apartments', methods=['GET'])
def getApartments():
    name = request.args.get('name', '')
    pool = request.args.get('pool', '')
    gym = request.args.get('gym', '')
    incldUtilities = request.args.get('incldUtilities', '')
    shuttleRte = request.args.get('shuttleRte', '')
    indvLeasing = request.args.get('indvLeasing', '')
    wsherDryer = request.args.get('wsherDryer', '')
    furnished = request.args.get('furnished', '')
    rmMatching = request.args.get('rmMatching', '')

    apartments = Apartment.query

    if pool:
        apartments = apartments.filter(Apartment.pool)
    if gym:
        apartments = apartments.filter(Apartment.gym == gym)
    if incldUtilities:
        apartments = apartments.filter(Apartment.incldUtilities)
    if shuttleRte:
        apartments = apartments.filter(Apartment.shuttleRte)
    if indvLeasing:
        apartments = apartments.filter(Apartment.indvLeasing)
    if wsherDryer:
        apartments = apartments.filter(Apartment.wsherDryer)
    if furnished:
        apartments = apartments.filter(Apartment.furnished)
    if rmMatching:
        apartments = apartments.filter(Apartment.rmMatching)
    if name:
        apartments = apartments.filter(Apartment.name==name)
    print(apartments)
    apartments_list = [apartment.to_dict() for apartment in apartments]
    return jsonify(apartments_list)


#TODO delete apartments, might not need route unless we want to let users delete them


if __name__ == '__main__':
  app.run(debug=True)
