import asyncio
from konlpy.tag import Okt
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

embeddings = HuggingFaceEmbeddings(
    model_name="jhgan/ko-sroberta-multitask", encode_kwargs={'normalize_embeddings': True}
)

async def load_faiss_cpu_db(db_index):
    db = FAISS.load_local(db_index, embeddings, allow_dangerous_deserialization=True)
    return db

async def search_faiss_cpu_db(query, db, k=5):
    query = ''.join(Okt().nouns(query)[::-1]) + query
    embedding_vector = await embeddings.aembed_query(query)

    docs_and_scores = await db.asimilarity_search_with_score(query, k=k)

    score = docs_and_scores[0][1]
    is_ambiguous = False
    is_food = True
    if score > 0.10:
        is_ambiguous = True
    elif score > 0.50:
        is_food = False
    ingredients = docs_and_scores[0][0].metadata['ingredients']
    ingredients = ingredients.replace('\b', '').replace('\n', '').replace('\t', '').strip()
    return ingredients, is_ambiguous, is_food