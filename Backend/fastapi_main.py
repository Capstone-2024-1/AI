import logging
from logging.handlers import RotatingFileHandler
import uvicorn
from fastapi import FastAPI, Query
from fastapi_services import load_faiss_cpu_db, search_faiss_cpu_db, infer_ingredients
from fastapi_models import SearchResponse, InferenceResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn.info")

app = FastAPI()
db = None

@app.on_event("startup")
async def startup_event():
    global db
    db = await load_faiss_cpu_db('../BuildingDB/SAFEAT_ASYNC_DB_INDEX')

@app.get("/search", response_model=SearchResponse)
async def search(koreanName: str = Query(..., example="김치찌개")):
    ingredients, is_ambiguous, is_food = await search_faiss_cpu_db(koreanName, db)
    ingredients = ingredients.replace("[", "").replace("]", "").replace("'", "").split(",")
    
    for i in range(len(ingredients)):
        ingredients[i] = ingredients[i].strip()
    ingredient_responses = [{"englishName": ingredient} for ingredient in ingredients]
    return SearchResponse(koreanName=koreanName, ingredients=ingredient_responses, isAmbiguous=is_ambiguous, isFood=is_food)

@app.get("/inference", response_model=InferenceResponse)
async def inference(koreanName: str = Query(..., example="삼겹살김치찌개")):
    ingredients = await infer_ingredients(koreanName)
    ingredient_responses = [{"englishName": ingredient} for ingredient in ingredients]
    return InferenceResponse(koreanName=koreanName, ingredients=ingredient_responses)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config="./logging_config.yaml")