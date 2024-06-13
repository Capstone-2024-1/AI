import asyncio
import time

from konlpy.tag import Okt
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from InferenceRecipe import IngredientInferencer
from Logging.ResultLogger import ResultLogger

embeddings = HuggingFaceEmbeddings(
    model_name="jhgan/ko-sroberta-multitask", encode_kwargs={'normalize_embeddings': True}
)

logger = ResultLogger()
ingredient_inferencer = IngredientInferencer.IngredientInferencer(logger)

async def load_faiss_cpu_db(db_index):
    db = FAISS.load_local(db_index, embeddings, allow_dangerous_deserialization=True)
    return db

async def search_faiss_cpu_db(query, db, k=5):
    original_query = query
    query = ''.join(Okt().nouns(query.replace(' ', ''))[::-1]) + query.replace(' ', '')
    embedding_vector = await embeddings.aembed_query(query)

    docs_and_scores = await db.asimilarity_search_with_score(query, k=k)

    score = docs_and_scores[0][1]
    is_ambiguous = False
    is_food = True
    if score > 0.15:
        is_ambiguous = True
    if score > 0.50:
        is_food = False
    ingredients = docs_and_scores[0][0].metadata['ingredients']
    ingredients = ingredients.replace('\b', '').replace('\n', '').replace('\t', '').strip()
    log_msg = str(time.time())+ " | " +  "검색어 : " + original_query + " | " + "검색된 음식 : " + docs_and_scores[0].page_content + "\n" + "검색된 재료 : " + ingredients + "\n" + "L2거리 : " + str(score) + " | " + "is_ambiguous : " + str(is_ambiguous) + " | " + "is_food : " + str(is_food)
    logger.log(log_msg, False)
    return ingredients, is_ambiguous, is_food

async def infer_ingredients(koreanName):
    ingredients = await ingredient_inferencer.infer(koreanName)
    ingredients = list(set(ingredients))
    return ingredients
