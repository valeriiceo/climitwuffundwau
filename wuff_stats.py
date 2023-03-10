from collections import Counter
import csv
import requests
from rich import print

URL = 'https://data.stadt-zuerich.ch/dataset/sid_stapo_hundenamen_od1002/download/KUL100OD1002.csv'


def read_data():
    try:
        response = requests.get(URL)
        response.encoding = "utf-8-sig"
        lines = response.text.splitlines()
        return csv.DictReader(lines)
    except Exception as e:
        return e


def male_count():
    dogs = read_data()
    m = Counter([dog['HundenameText'] for dog in dogs if dog['SexHundLang'] == 'männlich'])
    return m


def female_count():
    dogs = read_data()
    f = Counter([dog['HundenameText'] for dog in dogs if dog['SexHundLang'] == 'weiblich'])
    return f


def stats():
    dogs = read_data()
    name_counts = Counter([dog['HundenameText'] for dog in dogs])

    male_counter = male_count()
    female_counter = female_count()

    top_10_common = name_counts.most_common(10)
    top_10_male = male_counter.most_common(10)
    top_10_female = female_counter.most_common(10)

    shortest_name = min([name for name in name_counts if '?' not in name], key=len)
    longest_name = max(name_counts, key=len)

    print(f'Shortest Name: {shortest_name}')
    print(f'Longest Name: {longest_name}\n')

    print("Top 10 most common names overall:")
    for name, count in top_10_common:
        print(f"{name}: {count}")

    print(f'\nTop 10 most common male: ')
    for name, count in top_10_male:
        print(f"{name}: {count}")

    print(f'\nTop 10 most common female: ')
    for name, count in top_10_female:
        print(f"{name}: {count}")

    print(f'\nNumber of male dogs: {len(male_counter)}')
    print(f'Number of female dogs: {len(female_counter)}')
