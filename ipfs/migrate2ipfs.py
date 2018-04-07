#Python script

#query db for every currently served crs report
#get location of crs report
#move report to ipfs return ipfs hash to item db
#

#### Dependencies
import pymongo
import re
import sys
import time
import ipfsapi
from pathlib import Path

#### In bash
#mkdir ~/ipfs
#export IPFS_PATH=~/ipfs
# sudo ipfs daemon

#### Variables
dbname = "crs"
collection = "reports"
home = str(Path.home())
path_current = home +"/reports/"
ipfs_path = home + "/ipfs/"
api = ipfsapi.connect('127.0.0.1', 5001)


# Connect to DB and collection
# If standard 27017 port
# client = pymongo.MongoClient()             #client.close()
client = pymongo.MongoClient("localhost", 29017, maxPoolSize=50)
db = getattr(client, dbname)

db_resp = "Begin_Value"
while db_resp is not None:
    # Get a CRS sha 256 file with no ipfs hash
    db_resp = db.reports.find_one({"parsed_metadata.serve": "1", "ipfs_hash": {'$exists': False}}, {"sha256":1, "_id":1})

    print(db_resp['sha256'])

    # Add file to ipfs
    response = api.add(path_current + db_resp['sha256'])
    # {'Hash': 'QmbFMke1KXqnYyBBWxB74N4c5SBnJMVAiMNRcGu6x1AwQH', 'Name': 'test.txt'}

    key = {'_id':  db_resp['_id']}
    update_details = {'ipfs_hash': response['Hash']}

    db.reports.update(key, {"$set": update_details}, upsert=True)
    print(db_resp['_id'])
    
    #data_base = getCollection(dbname)
    #url_sourcesObject = getattr(data_base, collection)
    #db.reports.find({"parsed_metadata.serve": "1"},{"sha256":1, "_id":0}).count()

