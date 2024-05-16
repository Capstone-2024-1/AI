import os
import csv

food_categories = {
    "Crustaceans": ["Shrimp", "Crab", "Other crustaceans","Abalone", "Oyster", "Mussel", "Other shellfish"],
    "Dairy": ["Milk", "Soy milk", "Cheese", "Butter", "Other dairy products"],
    "Eggs": ["Eggs"],
    "Fish": ["Mackerel", "Other fish", "Other mollusks", "Other seafood"],
    "Fruiting Vegetables": ["Cucumber", "Chilly", "Tomato", "Other fruiting vegetables"],
    "Fruits": ["Apple", "Kiwi", "Peach", "Banana", "Mango", "Other fruits"],
    "Grains": ["Rice", "Wheat", "Corn", "Buckwheat", "Beans", "Barley", "Other grains"],
    "Herbage Crop": ["Onion", "Garlic", "Green onion", "Chives", "Other herbage crop"],
    "Meat": ["Beef", "Pork","Chicken", "Duck", "Lamb", "Horse meat"],
    "Nuts": ["Walnut", "Almond", "Pistachio", "Hazelnut", "Pinenuts", "Peanut", "Other nuts"],
    "Root Vegetables": ["Potato", "Sweet potato", "Radish", "wild chive", "Other root vegetables"],
    "Seasonings": ["Pepper",  "Pepper", "Ginger", "Honey", "Other seasonings"],
}

for key in food_categories.keys():
    ingredients = set()
    with open('is_included/'+key+'/is_included_' + key + '.csv', 'r', encoding='utf-8', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if '.' in row[1]:
                ingredients.add(row[0])
    ingredients = list(ingredients)
    ingredients.sort()

    for food_categorie in food_categories[key]:
        with open('is_included/' + key + '/is_included_' + key + '_' + food_categorie + '.csv', 'w', encoding='utf-8',
                  newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Ingredient', 'is_included'])
            for ingredient in ingredients:
                if ingredient == 'is_included':
                    continue
                writer.writerow([ingredient, ''])
