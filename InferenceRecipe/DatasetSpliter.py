import random

path = 'dataset_v2.jsonl'

def split_dataset(path, train_ratio=0.8, val_ratio=0.2):
    with open(path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    random.shuffle(lines)

    train_size = int(len(lines) * train_ratio)

    train_data = lines[:train_size]
    val_data = lines[train_size:]

    with open('v2_train.jsonl', 'w', encoding='utf-8') as file:
        for data in train_data:
            file.write(data)

    with open('v2_val.jsonl', 'w', encoding='utf-8') as file:
        for data in val_data:
            file.write(data)

split_dataset(path)
print("Dataset split into train and validation sets")



