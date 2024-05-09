import csv

file_path = 'cleaned_ingredients_with_hand.csv'

ingredients = set()
with open(file_path, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        ingredients.add(row[1])

ingredients = list(ingredients)
ingredients.sort()
food_categories = {
    "Fruits": ["Apple", "Kiwi", "Tomato", "Peach", "Banana", "Mango", "Other fruits"],
    "Nuts": ["Walnut", "Almond", "Pistachio", "Hazelnut", "Pinenuts", "Peanut", "Other nuts"],
    "Herbage Crop": ["Onion", "Garlic", "Green onion", "Chives", "Other herbage crop"],
    "Root Vegetables": ["Potato", "Sweet potato", "Radish", "wild chive", "Other root vegetables"],
    "Fruiting Vegetables": ["Cucumber", "Pepper", "Other fruiting vegetables"],
    "Grains": ["Rice", "Wheat", "Corn", "Buckwheat"],
    "Meat": ["Beef", "Pork"],
    "Poultry": ["Chicken", "Duck", "Lamb", "Horse meat"],
    "Eggs": ["Eggs"],
    "Seafood": ["Other seafood"],
    "Fish": ["Mackerel", "Other fish", "Other mollusks"],
    "Crustaceans": ["Shrimp", "Crab", "Other crustaceans"],
    "Shellfish": ["Abalone", "Oyster", "Mussel", "Other shellfish"],
    "Seasonings": ["Sugar", "Salt", "Pepper", "Ginger", "Honey", "Other seasonings"],
    "Dairy": ["Milk", "Soy milk", "Cheese", "Butter", "Other dairy products"],
    "Gluten": ["Gluten"]
}

import os

for key in food_categories.keys():
    if not os.path.exists('is_included/' + key):
        os.makedirs('is_included/' + key)
    with open('is_included/' + key + '/is_included_' + key + '.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Ingredient', 'is_included'])
        for ingredient in ingredients:
            if ingredient == 'Cleaned Ingredient' or ingredient == '' or ingredient == None or ingredient == ' ' or ingredient == 'cleaned_ingredients_with_original.csv':
                continue
            writer.writerow([ingredient, ''])