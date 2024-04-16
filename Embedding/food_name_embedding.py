from langchain_community.embeddings import HuggingFaceEmbeddings
from konlpy.tag import Okt
import asyncio

async def get_embedding_vector(query):
    # 형태소 분석기 인스턴스 생성
    okt = Okt()

    # query에서 명사만 추출하고 순서를 뒤집은 뒤 원래 query를 추가
    processed_query = ''.join(okt.nouns(query)[::-1]) + query

    # 임베딩 모델 초기화
    embeddings = HuggingFaceEmbeddings(
        model_name="jhgan/ko-sroberta-multitask",
        encode_kwargs={'normalize_embeddings': True}
    )

    # 비동기로 쿼리 임베딩
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

