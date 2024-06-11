import asyncio
from konlpy.tag import Okt
ingredients = ['Fruits', 'Nuts', 'Soy milk', 'Vegetables', 'Meat', 'Grain', 'Eggs', 'Seafood', 'Seasonings', 'Dairy', 'Apple', 'Kiwi', 'Peach', 'Banana', 'Mango', 'Other fruits', 'Walnut', 'Almond', 'Pistachio', 'Hazelnut', 'Pinenuts', 'Peanut', 'Other nuts', 'herbage crop', 'Root Vegetables', 'Fruiting Vegetables', 'Onion', 'Garlic', 'Green onion', 'Chives', 'Other herbage crop', 'Potato', 'Sweet potato', 'Radish', 'wild chive', 'Other root vegetables', 'Cucumber', 'Chilly', 'Tomato', 'Other Fruiting Vegetables', 'Rice', 'Wheat', 'Barley', 'Corn', 'Buckwheat', 'Beans', 'Other Grains', 'Beef', 'Pork', 'Poultry', 'Lamb', 'Horse Meat', 'Chicken', 'Duck', 'fish', 'Mackerel', 'Other Fish', 'Other Mollusks', 'Crustaceans', 'Shrimp', 'Crab', 'Other Crustaceans', 'Shellfish', 'Abalone', 'Oyster', 'Mussel', 'Other Shellfish', 'Other seafood', 'Pepper', 'Ginger', 'Honey', 'Asafoetida', 'Other seasonings', 'Milk', 'Cheese', 'Butter', 'Other dairy products']
ingredients = [i.lower() for i in ingredients]

async def check_ingredient(ingredient):
    ingredient_list = eval(ingredient)
    ingredient_list = [i.lower() for i in ingredient_list]
    check = True
    invalid_list = []
    for i in ingredient_list:
        if i not in ingredients:
            check = False
            invalid_list.append(i)
    if invalid_list: print(invalid_list)
    return check

async def build_faiss_cpu_db():
    import csv
    reader1 = csv.reader(open('../Data_Cleaning/10000recipe/Tagged_Ingredients.csv', 'r', encoding='utf-8'))
    reader2 = csv.reader(open('../Data_Cleaning/foodsafetykorea/Tagged_Ingredients.csv', 'r', encoding='utf-8'))
    Documents = []

    class Document:
        def __init__(self, page_content, metadata):
            self.page_content = page_content
            self.metadata = metadata

        def __str__(self):
            metadata_str = ', '.join([f'{key}: {value}' for key, value in self.metadata.items()])
            return f"Document(\n    page_content='{self.page_content}', \n    metadata={{\n        {metadata_str}\n    }}\n)"

    for idx, row in enumerate(reader1):
        if idx == 0:
            continue
        name = row[0].replace(' ', '')
        page_content = ''.join(Okt().nouns(name)[::-1]) + name
        metadata = {'name': row[0], 'food_name': row[1], 'ingredients': row[3]}
        if await check_ingredient(row[3]):
            Documents.append(Document(page_content, metadata))
        else:
            print(f"Error: {row[0]}")

    for idx, row in enumerate(reader2):
        if idx == 0:
            continue
        page_content = ''.join(Okt().nouns(row[0].replace(' ', ''))[::-1]) + row[0].replace(' ', '')
        metadata = {'name': row[0], 'food_name': row[1], 'ingredients': row[3]}
        if await check_ingredient(row[3]):
            Documents.append(Document(page_content, metadata))
        else:
            print(f"Error: {row[0]}")

    with open('additional.txt', 'r', encoding='utf-8') as f:
        reader = f.readlines()

        for idx, row in enumerate(reader):
            first_comma = row.find(',')
            food_name = row[:first_comma].strip()
            ingredients = row[first_comma + 1:].strip()
            page_content = ''.join(Okt().nouns(food_name.replace(' ', ''))[::-1]) + food_name.replace(' ', '')
            metadata = {'name': food_name, 'food_name': food_name, 'ingredients': ingredients}
            if await check_ingredient(ingredients):
                Documents.append(Document(page_content, metadata))
            else:
                print(f"Error: {food_name}")


    from langchain_text_splitters import CharacterTextSplitter

    text_splitter = CharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=0,
        separator="\n"
    )
    docs = text_splitter.split_documents(Documents)

    from langchain_community.embeddings import HuggingFaceEmbeddings

    embeddings = HuggingFaceEmbeddings(
        model_name="jhgan/ko-sroberta-multitask", encode_kwargs={'normalize_embeddings': True}
    )

    from langchain_community.vectorstores import FAISS
    db = await FAISS.afrom_documents(docs, embeddings)

    DB_INDEX = "SAFEAT_ASYNC_DB_INDEX"
    db.save_local(DB_INDEX)

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
    query = query.replace(' ', '')
    query = ''.join(Okt().nouns(query)[::-1]) + query
    embedding_vector = await embeddings.aembed_query(query)

    docs_and_scores = await db.asimilarity_search_with_score(query, k=k)

    score = docs_and_scores[0][1]
    is_ambiguous = False
    if score > 0.15:
        is_ambiguous = True
    ingredients = docs_and_scores[0][0].metadata['ingredients']

    print(docs_and_scores[0])
    return ingredients, is_ambiguous
async def main():
    await build_faiss_cpu_db()
    db = await load_faiss_cpu_db('SAFEAT_ASYNC_DB_INDEX')

    while True:
        query = input("검색할 쿼리를 입력하세요: ")
        if query == 'exit':
            break
        await search_faiss_cpu_db(query, db)

if __name__ == '__main__':
    asyncio.run(main())