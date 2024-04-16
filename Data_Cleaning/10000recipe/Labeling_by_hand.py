import csv

file_path = 'cleaned_ingredients_by_re.csv'

ingredients = []
with open(file_path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        ingredients.append(row[0])

food_categories = {
    "Fruits": ["Apple", "Kiwi", "Tomato", "Peach", "Banana", "Other fruits"],
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

labels = list(food_categories.keys())

print("어느 레이블에 대해 레이블링을 할 것인가요?")
for idx, label in enumerate(labels):
    print(f"{idx}: {label}")

label_idx = int(input("레이블 번호를 입력해주세요: "))
label = labels[label_idx]

with open('labeled_ingredients_as_' + labels[label_idx] +
          '.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    for idx, ingredient in enumerate(ingredients):
        print(ingredient,": yes = 1, no = enter, before = 2")
        label = input()
        if label == '1':
            writer.writerow([ingredient])
        elif label == '2':
            print(ingredients[idx-1], ": yes = 1, no = enter")
            label = input()
            if label == '1':
                writer.writerow([ingredients[idx-1]])
            else:
                continue
        else:
            continue
print(labels[label_idx], "레이블링이 완료되었습니다.")