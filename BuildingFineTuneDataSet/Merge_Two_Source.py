import csv, os, ast
path_10000recipe = '../Data_Cleaning/10000recipe/Tagged_Ingredients.csv'
path_foodsafetykorea = '../Data_Cleaning/foodsafetykorea/Tagged_Ingredients.csv'

reader1 = csv.reader(open(path_10000recipe, 'r', encoding='utf-8'))
reader2 = csv.reader(open(path_foodsafetykorea, 'r', encoding='utf-8'))

tag_order = ['Abalone', 'Crab', 'Mussel', 'Other crustaceans', 'Oyster', 'Shrimp', 'Other shellfish', 'Butter', 'Cheese', 'Milk', 'Soy milk', 'Other dairy products', 'Eggs', 'Mackerel', 'Other fish', 'Other mollusks', 'Other seafood', 'Chilly', 'Cucumber', 'Tomato', 'Other fruiting vegetables', 'Apple', 'Banana', 'Kiwi', 'Mango', 'Peach', 'Other fruits', 'Barley', 'Beans', 'Buckwheat', 'Corn', 'Rice', 'Wheat', 'Other grains', 'Chives', 'Garlic', 'Green onion', 'Onion', 'Other herbage crop', 'Beef', 'Chicken', 'Duck', 'Lamb', 'Pork', 'Horse meat', 'Almond', 'Hazelnut', 'Peanut', 'Pinenuts', 'Pistachio', 'Walnut', 'Other nuts', 'Potato', 'Radish', 'Sweet potato', 'wild chive', 'Other root vegetables', 'Ginger', 'Honey', 'Pepper', 'Other seasonings']
order_dict = {tag: index for index, tag in enumerate(tag_order)}

new_file_path = 'merged_ingredients.csv'

new = []

for idx, row in enumerate(reader1):
    if idx == 0:
        continue

    new_row0 = row[0]
    new_row1 = row[2].replace("['',", '[').replace(", '']", ']').replace("'','", '').replace(", ''", ', ')
    new_row2 = sorted(ast.literal_eval(row[3]), key=lambda x: order_dict[x])
    new_row3 = "<food_name>" + new_row0 + "</food_name>" + "<ingredients>" + new_row1 + "</ingredients>" + "<tags>" + str(new_row2) + "</tags>"

    if new_row1 == '[]':
        continue
    if new_row2 == []:
        continue

    new.append([new_row0, new_row1, new_row2, new_row3])

for idx, row in enumerate(reader2):
    if idx == 0:
        continue

    new_row0 = row[0]
    new_row1 = row[2].replace("['',", '[').replace(", '']", ']').replace("'','", '').replace(", ''", ', ')
    new_row2 = sorted(ast.literal_eval(row[3]), key=lambda x: order_dict[x])
    new_row3 = "<food_name>" + new_row0 + "</food_name>" + "<ingredients>" + new_row1 + "</ingredients>" + "<tags>" + str(new_row2) + "</tags>"

    if new_row1 == '[]':
        continue
    if new_row2 == []:
        continue
    new.append([new_row0, new_row1, new_row2, new_row3])

with open(new_file_path, 'w', encoding='utf-8', newline='') as file:
    for row in new:
        writer = csv.writer(file)
        writer.writerow(row)
