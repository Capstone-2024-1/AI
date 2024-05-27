from openai import OpenAI
from dotenv import load_dotenv
from InferenceRecipe.PromptProducer import PromptProducer
import os
import re


class IngredientInferencer:
    def __init__(self, logger):
        load_dotenv()
        self.model = os.getenv('FINE_TUNED_MODEL_ID')
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("API key not found. Make sure it's set in the .env file.")
        self.client = OpenAI(api_key=self.api_key)
        self.tag_order = ['Abalone', 'Crab', 'Mussel', 'Other crustaceans', 'Oyster', 'Shrimp', 'Other shellfish',
                          'Butter', 'Cheese', 'Milk', 'Soy milk', 'Other dairy products', 'Eggs', 'Mackerel',
                          'Other fish', 'Other mollusks', 'Other seafood', 'Chilly', 'Cucumber', 'Tomato',
                          'Other fruiting vegetables', 'Apple', 'Banana', 'Kiwi', 'Mango', 'Peach', 'Other fruits',
                          'Barley', 'Beans', 'Buckwheat', 'Corn', 'Rice', 'Wheat', 'Other grains', 'Chives', 'Garlic',
                          'Green onion', 'Onion', 'Other herbage crop', 'Beef', 'Chicken', 'Duck', 'Lamb', 'Pork',
                          'Horse meat', 'Almond', 'Hazelnut', 'Peanut', 'Pinenuts', 'Pistachio', 'Walnut', 'Other nuts',
                          'Potato', 'Radish', 'Sweet potato', 'wild chive', 'Other root vegetables', 'Ginger', 'Honey',
                          'Pepper', 'Other seasonings']
        self.tag_order.sort(key=len, reverse=True)
        self.prompt_producer = PromptProducer()
        self.logger = logger

    async def clean_inference_result(self, input_str: str):
        pattern = r"\b(" + "|".join(re.escape(item.lower()) for item in self.tag_order) + r")\b"
        matches = re.findall(pattern, input_str.lower())
        included_strings = []

        for match in matches:
            if match in included_strings:
                continue
            original = next((orig for orig, lower in map(lambda x: (x, x.lower()), self.tag_order) if lower == match), None)
            if original:
                included_strings.append(original)

        return included_strings

    async def infer(self, food_name):
        prompt = await self.prompt_producer.produce(food_name)
        completion = self.client.completions.create(
            model=self.model,
            prompt=prompt,
            max_tokens=100,
            seed=2061316412,
            temperature=0
        )
        result = await self.clean_inference_result(completion.choices[0].text)
        self.logger.log(food_name+" : "+str(result) + "\n" + str(completion.choices[0]) + "\n", True)
        return result
