import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("API key not found. Make sure it's set in the .env file.")

client = OpenAI(api_key=api_key)

def create_fine_tuning_job(training_file_id, model='davinci-002'):
    response = client.fine_tuning.jobs.create(
        training_file=training_file_id,
        model=model
    )
    return response

training_file_id = os.getenv('TRAINING_FILE_ID')
response = create_fine_tuning_job(training_file_id)
print("Fine-tuning job response:")
print(response.model_dump_json(indent=2))


with open('create_fine_tuning_job.txt', 'w') as file:
    file.write(response.model_dump_json(indent=2))
print("Fine-tuning job created and response saved to create_fine_tuning_job.txt")
