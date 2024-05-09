import csv
file_path = '../../Crawling/run/10000recipe/data/meta_data.csv'

ingredients = []
with open(file_path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        ingredient = row[2].replace('[','').replace(']','').replace("'",'').split(',')
        ingredients.extend(ingredient)

ingredients = list(set(ingredients))
ingredients.sort()
ingredients.remove('')

with open('ingredients.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    for ingredient in ingredients:
        writer.writerow([ingredient])