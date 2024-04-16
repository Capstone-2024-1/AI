import uvicorn
from fastapi import FastAPI, Query
from fastapi_services import load_faiss_cpu_db, search_faiss_cpu_db
from fastapi_models import SearchResponse

app = FastAPI()
db = None

@app.on_event("startup")
async def startup_event():
    global db
    db = await load_faiss_cpu_db('../BuildingDB/SAFEAT_ASYNC_DB_INDEX')

@app.get("/search", response_model=SearchResponse)
async def search(koreanName: str = Query(..., example="김치찌개")):
    ingredients, is_ambiguous = await search_faiss_cpu_db(koreanName, db)
    ingredients = ingredients.replace("[", "").replace("]", "").replace("'", "").split(",")
    
    for i in range(len(ingredients)):
        ingredients[i] = ingredients[i].strip()
    ingredient_responses = [{"englishName": ingredient} for ingredient in ingredients]
    return SearchResponse(koreanName=koreanName, ingredients=ingredient_responses, isAmbiguous=is_ambiguous)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)