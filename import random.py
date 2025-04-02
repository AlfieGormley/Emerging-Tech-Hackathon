import random
from datetime import datetime
from faker import Faker
fake = Faker()

def Create_Household():

    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 2, 1)
    Date = fake.date_between(start_date=start_date, end_date=end_date)
    Occupants = random.randint(1,6)#people
    Gas = random.randint(700,1400)#Kw hours
    Electric = random.randint(200,350)#Kw hours
    Water = random.randint(4310,17000)#Liters
    Bill = [Date,Occupants,Gas,Electric,Water]
    return (Bill)

def main(i):
    households = []
    for x in range (i):
        households.append(Create_Household())
    return households

if __name__ == "__main__":
    print(main(5))