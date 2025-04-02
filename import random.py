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
            "gas_usage_kwh": random.randint(22, 45), #Kw hours      
            "electric_usage_kwh": random.randint(6, 11), #Kw hours
            "water_usage_liters": random.randint(139, 548) #Liters
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


#Generates readings for a week
def generate_week_readings():
    
    start_date = datetime.datetime(2025, 2, 1)
    readings = []
    
    #Generate 7 days of data
    for day in range(7):   
        date = start_date + timedelta(days=day)
        readings.append({
            "date": date.isoformat(),
            "gas_usage_kwh": random.uniform(22.5, 45),  # Use uniform for floating point values
            "electric_usage_kwh": random.uniform(5.0, 10.0),  # Random float for electricity
            "water_usage_liters": random.randint(139, 548)  # Integer for water usage
        })
        
    return readings


def simulation(household_id):
    
    #Fetch Household Document
    household = households_collection.find_one({"_id": household_id})
    
    if not household:
        print(f"Household with _id {household_id} not found.")
        return
    
    #Get the recent readings from the last week:
    previous_week_readings = household['readings'][-7:]  # Get the last 7 entries of the 'readings' array
    
    previous_total_gas_usage = 0
    previous_total_electric_usage = 0
    previous_total_water_usage = 0
    
    #Sum the total values 
    for reading in previous_week_readings:
        previous_total_gas_usage += reading['gas_usage_kwh']
        previous_total_electric_usage += reading['electric_usage_kwh']
        previous_total_water_usage += reading['water_usage_liters']
    
    print(f"Total Gas Usage Previous Week (kWh): {previous_total_gas_usage}")
    print(f"Total Electric Usage Previous Week (kWh): {previous_total_electric_usage}")
    print(f"Total Water Usage Previous Week(Liters): {previous_total_water_usage}")
    
    current_week_readings = generate_week_readings()
    
    current_total_gas_usage = 0
    current_total_electric_usage = 0
    current_total_water_usage = 0
    
    for reading in current_week_readings:
        current_total_gas_usage += reading['gas_usage_kwh']
        current_total_electric_usage += reading['electric_usage_kwh']
        current_total_water_usage += reading['water_usage_liters']
        
    
    print(f"Total Gas Usage Current Week (kWh): {current_total_gas_usage}")
    print(f"Total Electric Usage Current Week (kWh): {current_total_electric_usage}")
    print(f"Total Water Usage Current Week (Liters): {current_total_water_usage}")
    
    #Calculate Percentage Change
    percentage_change_gas = ((current_total_gas_usage - previous_total_gas_usage) / previous_total_gas_usage) * 100
    
    percentage_change_electric = ((current_total_electric_usage - previous_total_electric_usage) / previous_total_electric_usage) * 100
    
    percentage_change_water = ((current_total_water_usage - previous_total_water_usage) / previous_total_water_usage) * 100
     
    print("Percentage Change In Gas", percentage_change_gas)
    print("Percentage Change In Electric", percentage_change_electric)
    print("Percentage Change In Water", percentage_change_water)
    
    
    
    
    return current_week_readings

    
    





def main(i):
    
    #Number of households we want to generate
    households = [create_household_doc() for _ in range(100)]
    
    #Add to the households collection 
    #households_collection.insert_many(households)
    
    readings = simulation("87420e90f0a5412fa6df30557ec17bf6")
    
    return readings
    
    #return households

if __name__ == "__main__":
    print(main(1))