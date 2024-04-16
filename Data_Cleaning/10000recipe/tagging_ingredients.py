import os
import csv

food_categories = {
    "Fruits": ["Apple", "Kiwi", "Peach", "Banana", "Mango", "Other fruits"],
    "Nuts": ["Walnut", "Almond", "Pistachio", "Hazelnut", "Pinenuts", "Peanut", "Other nuts"],
    "Herbage Crop": ["Onion", "Garlic", "Green onion", "Chives", "Other herbage crop"],
    "Root Vegetables": ["Potato", "Sweet potato", "Radish", "wild chive", "Other root vegetables"],
    "Fruiting Vegetables": ["Cucumber", "Chilly", "Tomato", "Other fruiting vegetables"],
    "Grains": ["Rice", "Wheat", "Corn", "Buckwheat", "Beans", "Other grains"],
    "Meat": ["Beef", "Pork","Chicken", "Duck", "Lamb", "Horse meat"],
    "Eggs": ["Eggs"],
    "Seafood": ["Other seafood"],
    "Fish": ["Mackerel", "Other fish", "Other mollusks"],
    "Crustaceans": ["Shrimp", "Crab", "Other crustaceans"],
    "Shellfish": ["Abalone", "Oyster", "Mussel", "Other shellfish"],
    "Seasonings": ["Pepper",  "Pepper", "Ginger", "Honey", "Other seasonings"],
    "Dairy": ["Milk", "Soy milk", "Cheese", "Butter", "Other dairy products"],
}

def find_filltered_name(ingredient):
    with open('cleaned_ingredients_with_hand.csv', 'r', encoding='utf-8', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if ingredient == row[0]:
                return row[1]
    return ''

tag_dict = {}
with open('cleaned_ingredients_with_hand.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if row[1] != 'Cleaned Ingredient':
            tag_dict[row[1]] = []
for key in food_categories.keys():
    for value in food_categories[key]:
        with open('./is_included/' + key + '/is_included_' + key + '_' + value + '.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[1] == '.':
                    if row[0] == 'Ingredient':
                        continue
                    tag_dict[row[0]].append(value)


readed_csv = []
index = 0
with open('Ingredients.csv', 'r', encoding='utf-8', newline='') as infile:
    reader = csv.reader(infile)
    for row in reader:
        dish, description, ingredients = row
        if dish == 'name':
            continue
        ingredients = eval(ingredients)
        cleand_ingredient_names = []
        for ingredient in ingredients:
            cleand_ingredient_names.append(find_filltered_name(ingredient))
        cleand_ingredient_names = list(set(cleand_ingredient_names))
        readed_csv.append([dish, description, cleand_ingredient_names])
        print(index, "번째 요리 정재된 재료 이름 찾기 완료")
        index += 1


for key in food_categories.keys():
    for food_categorie in food_categories[key]:
        with open('is_included/' + key + '/is_included_' + key + '_' + food_categorie + '.csv', 'r',
                  encoding='utf-8', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if ingredient == row[0] and '.' in row[1]:
                    tag_dict[ingredient].append(row[1])

index = 0
with open('Tagged_Ingredients.csv', 'w', encoding='utf-8', newline='') as outfile:
    writer = csv.writer(outfile)
    for dish, description, cleand_ingredient_names in readed_csv:
        if dish == 'name':
            writer.writerow([dish, description, cleand_ingredient_names, 'tags'])
            continue
        tags = []
        for ingredient in cleand_ingredient_names:
            tags.extend(tag_dict[ingredient])
        tags = list(set(tags))
        writer.writerow([dish, description, cleand_ingredient_names, tags])
        print(index, [dish, description, cleand_ingredient_names, tags])
        index += 1

