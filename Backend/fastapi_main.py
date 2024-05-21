import uvicorn
from fastapi import FastAPI, Query
from fastapi_services import load_faiss_cpu_db, search_faiss_cpu_db, infer_ingredients
from fastapi_models import SearchResponse, InferenceResponse

app = FastAPI()
db = None

async def startup_event():
    global db
    db = await load_faiss_cpu_db('../BuildingDB/SAFEAT_ASYNC_DB_INDEX')


app.add_event_handler("startup", startup_event)

@app.get("/search", response_model=SearchResponse)
async def search(koreanName: str = Query(..., examples=["김치찌개", "제육볶음"])):
    ingredients, is_ambiguous, is_food = await search_faiss_cpu_db(koreanName, db)
    ingredients = ingredients.replace("[", "").replace("]", "").replace("'", "").split(",")

    for i in range(len(ingredients)):
        ingredients[i] = ingredients[i].strip()
    ingredient_responses = [{"englishName": ingredient} for ingredient in ingredients]
    return SearchResponse(koreanName=koreanName, ingredients=ingredient_responses, isAmbiguous=is_ambiguous,
                          isFood=is_food)


@app.get("/inference", response_model=InferenceResponse)
async def inference(koreanName: str = Query(..., examples=["삼겹살김치찌개", "오징어볶음"])):
    ingredients = await infer_ingredients(koreanName)
    ingredient_responses = [{"englishName": ingredient} for ingredient in ingredients]
    return InferenceResponse(koreanName=koreanName, ingredients=ingredient_responses)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
