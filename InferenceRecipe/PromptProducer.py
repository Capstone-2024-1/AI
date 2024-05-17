import asyncio
import csv
import os
from konlpy.tag import Okt
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
os.environ["TOKENIZERS_PARALLELISM"] = "false"

class PromptProducer:
    def __init__(self, embeddings = HuggingFaceEmbeddings(model_name="jhgan/ko-sroberta-multitask", encode_kwargs={'normalize_embeddings': True}), db_index='../BuildingDB/SAFEAT_ASYNC_DB_INDEX', csv_file='../BuildingFineTuneDataSet/merged_ingredients.csv'):
        self.foods = {}
        self.db_index = db_index
        self.csv_file = csv_file
        self.embeddings = embeddings
        self.tag_order = """['Abalone', 'Crab', 'Mussel', 'Other crustaceans', 'Oyster', 'Shrimp', 'Other shellfish', 'Butter', 'Cheese', 'Milk', 'Soy milk', 'Other dairy products', 'Eggs', 'Mackerel', 'Other fish', 'Other mollusks', 'Other seafood', 'Chilly', 'Cucumber', 'Tomato', 'Other fruiting vegetables', 'Apple', 'Banana', 'Kiwi', 'Mango', 'Peach', 'Other fruits', 'Barley', 'Beans', 'Buckwheat', 'Corn', 'Rice', 'Wheat', 'Other grains', 'Chives', 'Garlic', 'Green onion', 'Onion', 'Other herbage crop', 'Beef', 'Chicken', 'Duck', 'Lamb', 'Pork', 'Horse meat', 'Almond', 'Hazelnut', 'Peanut', 'Pinenuts', 'Pistachio', 'Walnut', 'Other nuts', 'Potato', 'Radish', 'Sweet potato', 'wild chive', 'Other root vegetables', 'Ginger', 'Honey', 'Pepper', 'Other seasonings']"""
        asyncio.run(self.load_db_and_csv())

    async def load_db_and_csv(self):
        self.db = await self.load_faiss_cpu_db(self.db_index)
        self.load_foods_from_csv(self.csv_file)

    async def load_faiss_cpu_db(self, db_index):
        db = FAISS.load_local(db_index, self.embeddings, allow_dangerous_deserialization=True)
        return db

    async def load_foods_from_csv(self, csv_file):
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] != '':
                    self.foods[row[0]] = row[3]

    async def produce(self, query, k=5):
        from langchain_community.embeddings import HuggingFaceEmbeddings

        embeddings = HuggingFaceEmbeddings(
            model_name="jhgan/ko-sroberta-multitask", encode_kwargs={'normalize_embeddings': True}
        )
        query = ''.join(Okt().nouns(query)[::-1]) + query
        embedding_vector = await embeddings.aembed_query(query)

        docs_and_scores = await self.db.asimilarity_search_with_score(query, k=k)

        searched = []
        cnt = 0
        for i in range(1, len(docs_and_scores)):
            score = docs_and_scores[0][1]
            name = docs_and_scores[0][0].metadata['name']

            if score > 0.3:
                break
            searched_name = docs_and_scores[i][0].metadata['name']
            if searched_name not in self.foods.keys():
                continue
            cnt += 1
            if cnt > 3:
                break

            searched.append(self.foods[searched_name])

        result = "Please return only the food ingredients for " + query + " in the form of one python list that corresponds to the tags below.\n"
        result += self.tag_order + '\n'
        result += "Please refer to the information on the food similar below.\n"
        for i in searched:
            result += i + '\n'
        return result

