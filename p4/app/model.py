from pickleshare import *

db = PickleShareDB('users')

from pymongo import MongoClient

client = MongoClient("mongo", 27017) # Conectar al servicio (docker) "mongo" en su puerto estandar
db2 = client.SampleCollections   # Elegimos la base de datos de ejemplo