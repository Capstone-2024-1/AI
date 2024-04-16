from langchain_community.embeddings import HuggingFaceEmbeddings
from konlpy.tag import Okt
import asyncio

async def get_embedding_vector(query):
    okt = Okt()

    processed_query = ''.join(okt.nouns(query)[::-1]) + query

    embeddings = HuggingFaceEmbeddings(
        model_name="jhgan/ko-sroberta-multitask",
        encode_kwargs={'normalize_embeddings': True}
    )

    embedding_vector = await embeddings.aembed_query(processed_query)

    return embedding_vector

async def main():
    query = input("검색할 쿼리를 입력하세요: ")
    if query == 'exit':
        return

    embedding_vector = await get_embedding_vector(query)
    print(embedding_vector)

if __name__ == '__main__':
    asyncio.run(main())

