import csv
file_path = '../../Crawling/run/foodsafetykorea/data/recipes.csv'

new_rows = []
with open(file_path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        new_row = [row[1], row[1], row[2].split(',')]
        for idx, ingredient in enumerate(new_row[2]):
            new_row[2][idx] = ingredient.strip()
        new_rows.append(new_row)

with open('ingredients2.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    for ingredient in new_rows:
        writer.writerow(ingredient)