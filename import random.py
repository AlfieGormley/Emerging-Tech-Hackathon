import random
from datetime import datetime, timedelta
import uuid
from pymongo import MongoClient
import datetime
from faker import Faker
fake = Faker()


#Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["council"] #Database Name
households_collection = db["households"]  #Collection name


#Currently Readings are Monthly Readings
def generate_meter_readings():
    
    start_date = datetime.datetime(2025, 1, 1)
    readings = []
    
    for day in range(31):
        date = start_date + timedelta(days=day)
        readings.append({
            "date": date.isoformat(),
            "gas_usage_kwh": random.randint(700, 1400), #Kw hours      
            "electric_usage_kwh": random.randint(200, 350), #Kw hours
            "water_usage_liters": random.randint(4310, 17000) #Liters
        })
    
    return readings


def create_household_doc():
    
    household_document = {
        "_id": uuid.uuid4().hex,            #Generates a random unique identifier converted to a hex string
        "occupants": random.randint(1, 6),
        "house_number": random.randint(1, 100),  # Random house number
        "road": fake.street_name(),
        "work_from_home": fake.boolean(),  # Random True/False for work from home
        "readings": generate_meter_readings()  # List of daily readings
    }
    
    return household_document




def main(i):
    
    households = [create_household_doc() for _ in range(100)]
    
    doc = create_household_doc()
    
    households_collection.insert_many(households)
    
    return households

if __name__ == "__main__":
    print(main(1))