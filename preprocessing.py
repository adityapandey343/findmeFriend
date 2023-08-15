from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()


def stem(text):
    l = []

    for i in text.split():
        l.append(ps.stem(i))

    return " ".join(l)


def pipeline(city, hobby, desc, aim):
    city = city.replace(" ", "").replace(" ", "")
    city_l = city.split()
    hobby_l = hobby.split()
    desc_l = desc.split()
    aim_l = aim.split()

    hobby_l = [i.replace(" ", "") for i in hobby_l]
    desc_l = [i.replace(" ", "") for i in desc_l]
    aim_l = [i.replace(" ", "") for i in aim_l]

    temp_tag = city_l + hobby_l + desc_l + aim_l
    temp_tag = " ".join(temp_tag)
    temp_tag = temp_tag.replace("  ", " ").replace("  ", " ")

    temp_tag = stem(temp_tag)
    return temp_tag



