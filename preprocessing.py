import pandas as pd
import numpy as np
import streamlit as st
import openpyxl



# df = pd.read_excel("dataset.xlsx")
#
# df = df[['Name', 'Age', 'City', 'Hobby', 'Description', 'Aim']]
#
# df['Hobby'] = df['Hobby'].apply(lambda x: x.split(', '))
# df['Description'] = df['Description'].apply(lambda x: x.split(' '))
# df['Aim'] = df['Aim'].apply(lambda x: x.split(' '))
# df['Age'] = df['Age'].apply(lambda x:str(x))
# df['Age'] = df['Age'].apply(lambda x: x.split(' '))
# df['City'] = df['City'].apply(lambda x: x.split(' '))
#
# df["Hobby"] = df["Hobby"].apply(lambda x:[i.replace(" ","")for i in x])
# df["Description"] = df["Description"].apply(lambda x:[i.replace(" ","")for i in x])
# df["Aim"] = df["Aim"].apply(lambda x:[i.replace(" ","")for i in x])
#
# df['tags'] = df['Age'] + df['City'] + df['Hobby'] + df['Description'] + df['Aim']
#
# df['tags'] = df["tags"].apply(lambda x:" ".join(x)).apply(lambda x:x.replace("  "," ")).apply(lambda x:x.replace("  "," "))

from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()


def stem(text):
    l = []

    for i in text.split():
        l.append(ps.stem(i))

    return " ".join(l)

# df = df[['Name', 'Age', 'tags']]
#
# df["tags"] = df["tags"].apply(stem)


def pipeline(age, city, hobby, desc, aim):
    city = city.replace(" ", "").replace(" ", "")
    city_l = city.split()
    age_str = str(age)
    age_l = age_str.split()
    hobby_l = hobby.split()
    desc_l = desc.split()
    aim_l = aim.split()

    hobby_l = [i.replace(" ", "") for i in hobby_l]
    desc_l = [i.replace(" ", "") for i in desc_l]
    aim_l = [i.replace(" ", "") for i in aim_l]

    temp_tag = age_l + city_l + hobby_l + desc_l + aim_l
    temp_tag = " ".join(temp_tag)
    temp_tag = temp_tag.replace("  ", " ").replace("  ", " ")

    temp_tag = stem(temp_tag)
    return temp_tag



