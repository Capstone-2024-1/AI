import json

def process_jsonl_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    processed_data = []

    for line in lines:
        try:
            json_object = json.loads(line)
            prompt = json_object['prompt']

            before_start = "]\nPlease refer to the information on the food similar below.\n"
            after_end = '\\n", "completion": "'

            start_index = prompt.find(before_start) + len(before_start)
            end_index = prompt.find(after_end)

            transformed_part = prompt[start_index:end_index].split('\n')
            json_style_part = "[\n"
            for html_line in transformed_part:
                parts = {
                    "food_name": "",
                    "ingredients": "",
                    "tags": ""
                }
                if "<food_name>" in html_line:
                    parts['food_name'] = html_line.split("<food_name>")[1].split("</food_name>")[0]
                if "<ingredients>" in html_line:
                    parts['ingredients'] = html_line.split("<ingredients>")[1].split("</ingredients>")[0]
                if "<tags>" in html_line:
                    parts['tags'] = html_line.split("<tags>")[1].split("</tags>")[0]
                json_style_part += json.dumps(parts, ensure_ascii=False)
                json_style_part += ',\n'
            json_style_part = json_style_part.rstrip(',\n') + "\n]"
            prompt = prompt[:start_index] + json_style_part + prompt[end_index:]
            json_object['prompt'] = prompt

            processed_data.append(json.dumps(json_object, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"Error processing line: {e}")
            continue

    with open(output_file, 'w', encoding='utf-8') as file:
        for data in processed_data:
            file.write(data)

process_jsonl_file('dataset.jsonl', 'dataset_v2.jsonl')
