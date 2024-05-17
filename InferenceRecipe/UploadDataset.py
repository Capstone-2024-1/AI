import os
import openai
from openai import OpenAI
from dotenv import load_dotenv
import csv
import json

def csv_to_jsonl(csv_file_path='../BuildingFineTuneDataSet/prompt_list.csv', jsonl_file_path='dataset.jsonl'):
    with open(csv_file_path, newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        with open(jsonl_file_path, 'w', encoding='utf-8') as jsonl_file:
            for row in csv_reader:
                if len(row) < 2:
                    continue
                if row[0] == '' or row[1] == '':
                    continue
                jsonl_line = {
                    "prompt": row[0],
                    "completion": row[1]
                }
                jsonl_file.write(json.dumps(jsonl_line, ensure_ascii=False) + '\n')

csv_to_jsonl()

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
organization = os.getenv('OPENAI_ORGANIZATION')
project = os.getenv('OPENAI_PROJECT_ID')

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("API key not found. Make sure it's set in the .env file.")

client = OpenAI(api_key=api_key)

def upload_file(file_path, purpose='fine-tune'):
    with open(file_path, 'rb') as file:
        response = client.files.create(file=file, purpose=purpose)
    return response

file_path = './dataset.jsonl'
response = upload_file(file_path)
print("Response:")
print(response.model_dump_json(indent=2))

def list_files():
    response = client.files.list()
    return response

file_list = list_files()
for file in file_list:
    print(f"ID: {file.id}, Filename: {file.filename}, Purpose: {file.purpose}, Status: {file.status}, Created At: {file.created_at}")
