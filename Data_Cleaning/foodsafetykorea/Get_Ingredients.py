input_path = '../../Crawling/run/foodsafetykorea/data/recipes.csv'
output_path = 'ingredients.csv'

import csv

ingredients = set()
with open(input_path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        for ingredient in row[2].split(','):
            ingredients.add(ingredient.strip())

ingredients = list(ingredients)

with open(output_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    for ingredient in ingredients:
        writer.writerow([ingredient])