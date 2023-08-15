import streamlit as st
import preprocessing
import pandas as pd
from pymongo import MongoClient
import cv2
import numpy as np
from PIL import Image
import os
from firebase_admin import credentials, storage, initialize_app

cred = credentials.Certificate("key.json")
try:
    app = initialize_app(cred, { 'storageBucket':'findfriend-bc6c4.appspot.com' })
except:
    pass


def header(url):
    st.markdown(f'<p style="color:#ffffff;font-size:60px;;">{url}</p>',unsafe_allow_html=True)

header("Find Me A Friend")

with open( "css\style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)



def display_friends(no_of_row, no_of_col):
    rows = no_of_row
    col = no_of_col
    for row in range(rows):
        for i, j in enumerate(st.columns(col)):
            with j:
                st.markdown(f" **:green[{name_list[i + (row * col)]}]** ")
                # display_img(f"{phn_list[i + (row * col)]}")
                get_image_from_firebase_and_display(f"{phn_list[i + (row * col)]}")
                st.markdown(f" **:blue[Phone: ]** {phn_list[i + (row * col)]}")
                st.markdown(f" **:blue[Age: ]** {age_list[i + (row * col)]}")
                st.markdown(f" **:blue[City: ]** {city_list[i + (row * col)]}")
                st.markdown(f" **:blue[Hobbies: ]** {hobby_list[i + (row * col)]}")
                st.markdown(f" **:blue[Description: ]** {desc_list[i + (row * col)]}")
                st.markdown(f" **:blue[Aim: ]** {aim_list[i + (row * col)]}")

def save_img(picture):
    bytes_data = picture.getvalue()
    img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    im_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    Image.fromarray(im_rgb).save(f'new_images/{phn}.jpg')

def display_img(phn):
    image = Image.open(f'new_images/{phn}.jpg')
    st.image(image)


def upload_img_to_firebase(picture):
    bytes_data = picture.getvalue()
    img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    im_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    Image.fromarray(im_rgb).save(f'{phn}.jpg')
    fileName = f"{phn}.jpg"
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)
    os.remove(f'{phn}.jpg')

def get_image_from_firebase_and_display(phn):
    phn = str(phn)
    bucket = storage.bucket()
    blob = bucket.get_blob(f"{phn}.jpg")
    arr = np.frombuffer(blob.download_as_string(), np.uint8)
    img = cv2.imdecode(arr, cv2.COLOR_BGR2RGB)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    image = Image.fromarray(img)
    st.image(image)


def recommend(person):
    name_list = []
    phn_list = []
    age_list = []
    city_list = []
    hobby_list = []
    desc_list = []
    aim_list = []

    index = df[df['Name'] == person].index[0]
    distances = similarity[index]
    friends_list = sorted(list(enumerate(distances)), reverse=True, key=(lambda x: x[1]))[1:]

    for i in friends_list:
        name_list.append(df.iloc[i[0]].Name)
        phn_list.append(df.iloc[i[0]].Phone)
        age_list.append(df.iloc[i[0]].Age)
        city_list.append(df.iloc[i[0]].City)
        hobby_list.append(df.iloc[i[0]].Hobby)
        desc_list.append(df.iloc[i[0]].Description)
        aim_list.append(df.iloc[i[0]].Aim)
    return name_list, phn_list, age_list, city_list, hobby_list, desc_list, aim_list



picture = st.camera_input("")
name = st.text_input('Name', '')
phn = st.text_input('Phone number', '')
age = st.slider('Age', min_value=0, max_value=100, value=0, step = 1)
city = st.text_input('City', '')
hobby = st.text_input('Hobbies / Interests', '')
desc = st.text_input('Describe yourself', '')
aim = st.text_input('Goals of life', '')
agree = st.checkbox('Should I add your details to our database ?')

phn = phn.replace(" ","")




if st.button("Find Friends") and age!=0 and name != "" and phn != "" and city != "" and hobby != "" and desc != "" and aim != "" and picture is not None:
    client = MongoClient("mongodb+srv://aditya123:6AUedsUnVL7QHiJ@cluster0.rghxolj.mongodb.net/")
    db = client['friends_db']
    collection = db["friends_collection"]


    if agree:
        if len(list(collection.find({"Phone": phn}))) > 0:
            myquery = {"Phone": phn}
            collection.delete_one(myquery)
        dict = {'Name': name, 'Phone': phn, 'Age': age, 'City': city, 'Hobby': hobby, 'Description': desc, 'Aim': aim}
        collection.insert_one(dict)
        upload_img_to_firebase(picture)


    # creating a new dataframe
    df = pd.DataFrame(columns=['Name', 'Phone', 'Age', 'City', 'Hobby', 'Description', 'Aim', 'Tags'])


    # entering new entry in dataframe
    if len(list(collection.find({"Phone": phn}))) == 0:
        tags = preprocessing.pipeline(city, hobby, desc, aim)
        df.loc[len(df.index)] = [name, phn, age, city, hobby, desc, aim, tags]



    friend_list = list(collection.find()) # calling out data from mongoDB into list
    # inserting entries from database into dataframe
    for i in friend_list:
        tags = preprocessing.pipeline(i['City'], i['Hobby'], i['Description'], i['Aim'])
        df.loc[len(df.index)] = [i['Name'], i['Phone'], i['Age'], i['City'], i['Hobby'], i['Description'], i['Aim'], tags]



    from sklearn.feature_extraction.text import CountVectorizer
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(df['Tags']).toarray()



    from sklearn.metrics.pairwise import cosine_similarity
    similarity = cosine_similarity(vectors)


    # Using recommed function
    name_list, phn_list, age_list, city_list, hobby_list, desc_list, aim_list = recommend(name)
    display_friends(5,2)



else:
    st.markdown("**_:red[Fill all the details carefully.]_**")




import base64


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
        unsafe_allow_html=True
    )


add_bg_from_local('Krishna.png')












