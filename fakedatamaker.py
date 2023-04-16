from models import User, Messages, Sublease, Apartment, db
from faker import Faker
import random

fake = Faker()

apartment_names =  ['The Outpost', 'The Thompson', 'Bobcat Village', 'College Town San Marcos', 'Vie Lofts at San Marcos', 'Dakota Ranch Student Apartments', 'The Grove at San marcos', 'Uptown Square', 'The Junction San Marcos', 'The View on the Square', 'Westfield Apartments', 'The Village on Telluride', 'The Cottages at San Marcos' 'The Lodge Apartments', 'Arba', 'Bishops Square', 'The Avenue at San Marcos', 'Copper Beech at San Marcos', 'Cheatham Street Flats', 'redpoint San Marcos', 'Sanctuary Lofts', 'Millenium on Post', 'The Retreat', 'Elevation on Post', 'The Lyndon at Springtown', 'The Social SMTX', 'The Local Downtown', 'Vistas San Marcos', 'The Oasis San Marcos', 'Highcrest Apartments', 'The Timbers', 'Hill Country Apartments', 'Vintage Pads Apartments', 'Leah Avenue Townhomes', 'CastleRock at San Marcos', 'Villagio Apartments', 'The Fitzroy San Marcos', 'The Edge', 'Pointe San Marcos', 'Riverside Ranch', 'The Parlor', 'River Oaks Villas Apartments', 'Sadler House Apartments', 'Hawthorne at Blanco Riverwalk', 'Springmarc', 'Savannah Club Apartments', 'Sutton Apartments', 'Mosscliff Apartments', 'Encino Pointe']
def addfakedata():
    for aptname in apartment_names:
        newApartment = Apartment(
            name = aptname,
            pets = fake.boolean(),
            pool = fake.boolean(),
            gym = fake.boolean(),
            incldUtilities = fake.boolean(),
            shuttleRte = fake.boolean(),
            indvLeasing = fake.boolean(),
            wsherDryer = fake.boolean(),
            furnished = fake.boolean(),
            rmMatching = fake.boolean(),
            rating = random.randint(0,5),
            phone = fake.phone_number(),
            link = fake.url(),
        )
        db.session.add(newApartment)

    db.session.commit()