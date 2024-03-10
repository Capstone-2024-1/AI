import csv
import os
from Crawling.Crawler import Crawler_10000recipe

file_list = os.listdir('data/names')
names = set()
for file in file_list:
    with open(f'./data/names/{file}', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            names.add(row[0])

file_list = os.listdir('data/meta_data')
meta_data = []
for file in file_list:
    with open(f'./data/meta_data/{file}', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] in names and row not in meta_data:
                meta_data.append(row)

file_list = os.listdir('data/timeoutlist')
timeoutlist = set()
for file in file_list:
    with open(f'./data/timeoutlist/{file}', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            timeoutlist.add((row[0], row[1]))

with open('data/names.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    for row in names:
        writer.writerow([row])

with open('data/meta_data.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    for row in meta_data:
        writer.writerow(row)

with open('data/timeoutlist.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    for row in timeoutlist:
        writer.writerow([row[0], row[1]])

crawler = Crawler_10000recipe()
result = []
for row in timeoutlist:
    if (row[0] == "name" and row[1] == "href") or "java" in row[1]:
        continue
    tmp = crawler.__get_meta_data__("https://www.10000recipe.com"+row[1], row[0])
    if tmp['ingredients'] == [] or tmp['ingredients'] == {}:
        continue
    result.append({'name': row[0], 'food_name': tmp['food_name'], 'ingredients': tmp['ingredients']})
checker = set()

with open('data/meta_data.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if (row[0] not in checker and row[2] == []) or row[0] in checker:
            continue
        checker.add(row[0])
        result.append({'name': row[0], 'food_name': row[1], 'ingredients': row[2]})

with open('data/meta_data.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    for row in result:
        writer.writerow([row['name'], row['food_name'], row['ingredients']])


