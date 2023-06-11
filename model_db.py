from pymongo import MongoClient
import pymongo
from decouple import config

CONNECTION_STRING = config('CONNECTION_STRING')

def get_database():

    client = MongoClient(CONNECTION_STRING)
    db = client.mydb
    return db

# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":
    # Get the database
    client = MongoClient(CONNECTION_STRING)
    db = client.get_database()
    response = list(db.spatial_tile38.find({}))
    count=0
    for r in response:
        count=count+1;

    print(count)
