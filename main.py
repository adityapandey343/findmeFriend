import streamlit as st
import preprocessing
import pandas as pd
from pymongo import MongoClient
import cv2
import numpy as np
from PIL import Image
import os


def save_img(picture):
    bytes_data = picture.getvalue()
    img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    im_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    Image.fromarray(im_rgb).save(f'images/{phn}.jpg')

def display_img(phn):
    image = Image.open(f'images/{phn}.jpg')
    st.image(image)

def recommend(person):
    name_list = []
    phn_list = []

    index = df[df['Name'] == person].index[0]
    distances = similarity[index]
    friends_list = sorted(list(enumerate(distances)), reverse=True, key=(lambda x: x[1]))[1:6]

    for i in friends_list:
        name_list.append(df.iloc[i[0]].Name)
        phn_list.append(df.iloc[i[0]].Phone)
    return name_list, phn_list




st.header("**:red[Find Me a Friend]**")
# Taking INPUTS

picture = st.camera_input("")
name = st.text_input('Name', '')
phn = st.text_input('Phone number', '')
age = st.slider('Age', min_value=0, max_value=100, value=0, step = 1)
city = st.text_input('City', '')
hobby = st.text_input('Hobbies / Interests', '')
desc = st.text_input('Describe yourself', '')
aim = st.text_input('Goals of life', '')
agree = st.checkbox('Should I add your details to our database ?')



if st.button("Find Friends") and age!=0 and name != "" and phn != "" and city != "" and hobby != "" and desc != "" and aim != "" and picture is not None:
    client = MongoClient("mongodb://localhost:27017/")
    db = client['friends_db']
    collection = db["friends_collection"]
    friend_list = list(collection.find())

    if len(list(collection.find({"Phone": phn}))) > 0 and agree:
        myquery = {"Phone": phn}
        collection.delete_one(myquery)
        dict = {'Name': name, 'Phone': phn, 'Age': age, 'City': city, 'Hobby': hobby, 'Description': desc, 'Aim': aim}
        collection.insert_one(dict)
        try:
            os.remove(f"images/{phn}.jpg")
        except:
            if picture is not None:
                save_img(picture)

    if len(list(collection.find({"Phone": phn}))) == 0 and agree:
        dict = {'Name': name, 'Phone': phn, 'Age': age, 'City': city, 'Hobby': hobby, 'Description': desc, 'Aim': aim}
        collection.insert_one(dict)
        if picture is not None:
            save_img(picture)




    # creating a new dataframe
    df = pd.DataFrame(columns=['Name', 'Phone', 'Age', 'City', 'Hobby', 'Description', 'Aim', 'Tags'])


    # entering new entry in dataframe
    if len(list(collection.find({"Phone": phn}))) == 0:
        tags = preprocessing.pipeline(age, city, hobby, desc, aim)
        df.loc[len(df.index)] = [name, phn, age, city, hobby, desc, aim, tags]


    # inserting entries from database into dataframe
    for i in friend_list:
        tags = preprocessing.pipeline(i['Age'], i['City'], i['Hobby'], i['Description'], i['Aim'])
        df.loc[len(df.index)] = [i['Name'], i['Phone'], i['Age'], i['City'], i['Hobby'], i['Description'], i['Aim'], tags]







    from sklearn.feature_extraction.text import CountVectorizer
    cv = CountVectorizer(max_features=5000, stop_words='english')

    vectors = cv.fit_transform(df['Tags']).toarray()




    from sklearn.metrics.pairwise import cosine_similarity

    similarity = cosine_similarity(vectors)

    # print(sorted(list(enumerate(similarity[0])), reverse=True, key=(lambda x: x[1]))[1:6])


    name_list, phn_list = recommend(name)


    col1, col2, col3 = st.columns(3)
    with col1:
        st.header(f"{name_list[0]}")
        display_img(f"{phn_list[0]}")
        st.write(f"Phone: {phn_list[0]}")

    with col2:
        st.header(f"{name_list[1]}")
        display_img(f"{phn_list[1]}")
        st.write(f"Phone: {phn_list[1]}")

    with col3:
        st.header(f"{name_list[2]}")
        display_img(f"{phn_list[2]}")
        st.write(f"Phone: {phn_list[2]}")



















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


add_bg_from_local('Krishna.jpg')











