import pandas as pd

with open('dataset.txt', 'r') as file:
    data = file.read().replace('\n', "")


names = []

for i in range(len(data)):
    if (data[i:i+5] == "Name:"):
        i = i+6
        name = ""
        while(data[i] != " "):
            name = name + (data[i])
            i+=1
        names.append(name)

ages = []

for i in range(len(data)):
    if (data[i:i+4] == "Age:"):
        i = i+5
        age = ""
        while(data[i] != " "):
            age = age + (data[i])
            i+=1
        ages.append(age)

cities = []

for i in range(len(data)):
    if (data[i:i+5] == "City:"):
        i = i+6
        city = ""
        while(data[i] != " "):
            city = city + data[i]
            i+=1
        cities.append(city)

hobbies = []

for i in range(len(data)):
    if (data[i:i+20] == "Hobbies / Interests:"):
        i = i+21
        hobby = ""
        while(data[i:i+5] != "Descr"):
            hobby = hobby + data[i]
            i+=1
        hobbies.append(hobby)

descriptions = []

for i in range(len(data)):
    if (data[i:i+12] == "Description:"):
        i = i+13
        description = ""
        while(data[i:i+3] != "Aim"):
            description = description + data[i]
            i+=1
        descriptions.append(description)

aims = []

for i in range(len(data)):
    if (data[i:i + 12] == "Aim of Life:"):
        i = i + 13
        aim = ""
        while (data[i] != "."):
            aim = aim + data[i]
            i += 1
        aims.append(aim)

    if (data[i:i + 13] == "Aims of Life:"):
        i = i + 14
        aim = ""
        while (data[i] != "."):
            aim = aim + data[i]
            i += 1
        aims.append(aim)

data_dict = {'Name': names,
            'Age': ages,
            'City': cities,
            'Hobby': hobbies,
            'Description': descriptions,
            'Aim': aims}

dataset = pd.DataFrame(data_dict)

for i in range(21):
    dataset.iloc[i,4]
    for j in range(len(dataset.iloc[i,4])):
        if(dataset.iloc[i,4][j] == '.'):
            dataset.iloc[i,4] = dataset.iloc[i,4][j+2:]
            break;

dataset.to_excel("dataset.xlsx")
