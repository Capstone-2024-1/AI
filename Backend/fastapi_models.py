from pydantic import BaseModel, Field

class IngredientResponse(BaseModel):
    englishName: str = Field(...)

class SearchResponse(BaseModel):
    koreanName: str
    ingredients: list[IngredientResponse]
    isAmbiguous: bool
    isFood: bool

class InferenceResponse(BaseModel):
    koreanName: str
    ingredients: list[IngredientResponse]
