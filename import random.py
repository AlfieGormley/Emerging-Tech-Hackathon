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
    
    
    
    
    
    
    # Respond based on the percentage change
    if percentage_change_gas < 0:
        print("Well done, you saved gas")
    elif percentage_change_gas > 0:
        print("Gas usage has increased")
    elif percentage_change_gas > 10:
        print("🚨 Gas usage has increased significantly! Investigate for possible issues.")
    elif percentage_change_gas < -10:
        print("✅ Gas usage has decreased significantly. Great job on saving!")
        
    
    if percentage_change_electric < 0:
        print("Well done you saved electric")
    elif percentage_change_electric > 0:
        print("Electric usage has increased")
    elif percentage_change_electric > 10:
        print("🚨 Electric usage has increased significantly! Check for issues.")
    elif percentage_change_electric < -10:
        print("✅ Electric usage has decreased significantly. Great energy saving!")
    
    
    # Check if water usage has decreased (negative percentage change)
    if percentage_change_water < 0:
        print("💧 Well done, you saved water!")
    elif percentage_change_water > 0:
        print("💧 Water usage has increased")
    elif percentage_change_water > 10:
        print("🚨 Water usage has increased significantly. Consider investigating for leaks.")
    elif percentage_change_water < -10:
        print("✅ Water usage has decreased significantly. Great job conserving water!")
        
    #Collect Weekly Averages
    weekly_averages, sorted_households = all_time_weekly_average()
    
    #Find Rank
    rank = find_household_index(household_id, sorted_households) + 1
    
    
    
    percentage_changes = {
        "gas_usage_percentage_change": percentage_change_gas,
        "weekly_gas_usage": current_total_gas_usage,
        
        
        "electric_usage_percentage_change": percentage_change_electric,
        "weekly_electric_usage": current_total_electric_usage,
        
        
        "water_usage_percentage_change": percentage_change_water,
        "weekly_water_usage": current_total_water_usage,
        
        "household_rank": rank
        
    }
    
    
    return percentage_changes

    

def find_household_index(search_id, sorted_households):
        for index, (household_id, data) in enumerate(sorted_households.items()):
            
            if household_id == search_id:
                return index  # Return the index of the matched household
            
        return -1  # Return -1 if the household is not found





#Calculates Weekly Averages And Sorts By Total Energy Consumption
def all_time_weekly_average():
    
    all_households = households_collection.find()
    
    household_weekly_averages = {}
    
    
    for household in all_households:
        household_id = household["_id"]
        readings = household.get('readings', [])
        
        
        num_weeks = len(readings) // 7  # Number of full weeks available
        
        if num_weeks == 0:
            continue  # Skip households with less than 7 days of data
        
        total_gas = sum(r["gas_usage_kwh"] for r in readings) / num_weeks
        total_electric = sum(r["electric_usage_kwh"] for r in readings) / num_weeks
        total_water = sum(r["water_usage_liters"] for r in readings) / num_weeks
        total_usage = total_gas + total_electric + total_water
        
        
        # Store in the dictionary with the _id as the key
        household_weekly_averages[household_id] = {
            "average_weekly_gas_usage": total_gas,
            "average_weekly_electric_usage": total_electric,
            "average_weekly_water_usage": total_water,
            "total_energy_consumption": total_usage
        }
        
    sorted_households = dict(sorted(household_weekly_averages.items(), key=lambda x: x[1]['total_energy_consumption']))
        
    return household_weekly_averages, sorted_households
                
    
    
def get_household_info(household_id, ranked_households):
    
    
    if household_id in ranked_households:
        info = ranked_households[household_id]
        return {
            'rank': info['rank'],
            'average_weekly_gas_usage': info['average_weekly_gas_usage'],
            'average_weekly_electric_usage': info['average_weekly_electric_usage'],
            'average_weekly_water_usage': info['average_weekly_water_usage'],
            'total_energy_consumption': info['total_energy_consumption']
        }
    else:
        return "Household ID not found."

    




def main(i):
    
    #Number of households we want to generate
    #households = [create_household_doc() for _ in range(100)]
    
    #Add to the households collection 
    #households_collection.insert_many(households)
    
    percentage_changes = simulation("87420e90f0a5412fa6df30557ec17bf6")
    
    print(percentage_changes)
    
    weekly_averages, sorted_households = all_time_weekly_average()
    
    #print(weekly_averages)
    #print(sorted_households)
    
    

    return 
    
    

if __name__ == "__main__":
    print(main(1))