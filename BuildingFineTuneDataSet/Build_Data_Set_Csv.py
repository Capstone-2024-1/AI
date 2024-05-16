import asyncio
import csv, os

from konlpy.tag import Okt

tag_order = """['Abalone', 'Crab', 'Mussel', 'Other crustaceans', 'Oyster', 'Shrimp', 'Other shellfish', 'Butter', 'Cheese', 'Milk', 'Soy milk', 'Other dairy products', 'Eggs', 'Mackerel', 'Other fish', 'Other mollusks', 'Other seafood', 'Chilly', 'Cucumber', 'Tomato', 'Other fruiting vegetables', 'Apple', 'Banana', 'Kiwi', 'Mango', 'Peach', 'Other fruits', 'Barley', 'Beans', 'Buckwheat', 'Corn', 'Rice', 'Wheat', 'Other grains', 'Chives', 'Garlic', 'Green onion', 'Onion', 'Other herbage crop', 'Beef', 'Chicken', 'Duck', 'Lamb', 'Pork', 'Horse meat', 'Almond', 'Hazelnut', 'Peanut', 'Pinenuts', 'Pistachio', 'Walnut', 'Other nuts', 'Potato', 'Radish', 'Sweet potato', 'wild chive', 'Other root vegetables', 'Ginger', 'Honey', 'Pepper', 'Other seasonings']"""

foods = {}
async def load_faiss_cpu_db(db_index):
    from langchain_community.embeddings import HuggingFaceEmbeddings

    embeddings = HuggingFaceEmbeddings(
        model_name="jhgan/ko-sroberta-multitask", encode_kwargs={'normalize_embeddings': True}
    )
    from langchain_community.vectorstores import FAISS
    db = FAISS.load_local(db_index, embeddings, allow_dangerous_deserialization=True)
    return db

async def search_faiss_cpu_db(query, db, k=5):
    from langchain_community.embeddings import HuggingFaceEmbeddings

    embeddings = HuggingFaceEmbeddings(
        model_name="jhgan/ko-sroberta-multitask", encode_kwargs={'normalize_embeddings': True}
    )
    query = ''.join(Okt().nouns(query)[::-1]) + query
    embedding_vector = await embeddings.aembed_query(query)

    docs_and_scores = await db.asimilarity_search_with_score(query, k=k)

    searched = []
    cnt = 0
    for i in range(1, len(docs_and_scores)):
        score = docs_and_scores[0][1]
        name = docs_and_scores[0][0].metadata['name']

        if score > 0.3:
            break
        searched_name = docs_and_scores[i][0].metadata['name']
        if searched_name not in foods.keys():
            continue
        cnt += 1
        if cnt > 3:
            break

        searched.append(foods[searched_name])

    result1 = "Please return only the food ingredients for " + name + "in the form of a list that corresponds to the tags below.\n"
    result1 += tag_order + '\n'
    result1 += "Please refer to the information on the food similar below.\n"
    for i in searched:
        result1 += i + '\n'
    result2 = foods[name]
    result2 = result2.split('<tags>')[1].split('</tags>')[0]
    return result1, result2

async def build_dataset():
    db = await load_faiss_cpu_db('../BuildingDB/SAFEAT_ASYNC_DB_INDEX')

    prompt_list = []
    response_list = []

    with open('merged_ingredients.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        check = 0
        idx = 0
        for row in reader:
            query = row[0]
            prompt, response = await search_faiss_cpu_db(query, db)
            prompt_list.append(prompt)
            response_list.append(response)
            idx += 1
            print(idx,"번째 데이터 생성 완료")

    with open('prompt_list.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        for i in range(len(prompt_list)):
            writer.writerow([prompt_list[i], response_list[i]])


if __name__ == '__main__':
    with open('merged_ingredients.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] != '':
                foods[row[0]] = row[3]
    asyncio.run(build_dataset())
