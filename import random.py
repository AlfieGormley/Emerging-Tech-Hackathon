import random
from datetime import datetime, timedelta
from pymongo import MongoClient
import datetime
from faker import Faker
fake = Faker()


#Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["council"] #Database Name
households_collection = db["households"]  #Collection name




def Create_Household():

    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 2, 1)
    Date = fake.date_between(start_date=start_date, end_date=end_date)
    Occupants = random.randint(1,6)#people
    Gas = random.randint(700,1400)#Kw hours
    Electric = random.randint(200,350)#Kw hours
    Water = random.randint(4310,17000)#Liters
    
    meter_readings = [Date,Occupants,Gas,Electric,Water]
    
    return (meter_readings)



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
        "occupants": random.randint(1, 6),
        "house_number": random.randint(1, 100),  # Random house number
        "road": fake.street_name(),
        "work_from_home": fake.boolean(),  # Random True/False for work from home
        "readings": generate_meter_readings()  # List of daily readings
    }
    
    
    return household_document




def main(i):
    
    doc = create_household_doc()
    return doc

if __name__ == "__main__":
    print(main(1))