from pymongo import MongoClient
import json
import streamlit as st

client = MongoClient("mongodb+srv://aditya123:6AUedsUnVL7QHiJ@cluster0.rghxolj.mongodb.net/")

db = client['friends_db']
collection = db["friends_collection"]



    # client = MongoClient("mongodb://localhost:27017/")
    #
    # db = client['friends_db']
    # collection = db["friends_collection"]
    #
    # with open('dataset.json') as file:
    #     file_data = json.load(file)

    # if isinstance(file_data, list):
    #     collection.insert_many(file_data)
    # else:
    #     collection.insert_one(file_data)

    # friends_dat = collection.find()
    # one_data = collection.find_one()
    # friends_data_list = list(friends_dat)

    # db.collection.updateMany({}, {'$unset': {'Column1': ""}}, multi=True)

    # friends_dat = collection.find()
    # one_data = collection.find_one()
    # friends_data_list = list(friends_dat)









