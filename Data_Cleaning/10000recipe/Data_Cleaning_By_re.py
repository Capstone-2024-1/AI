import re
import csv

file_path = 'ingredients.csv'

def clean_ingredient(ingredient):
    units = ['ml', 'g', 'cm', '개', '인분', '송이', '마리', '년근', '컵', '봉지', '호', '배', '색', '분', '센티', '대', '큰술', '층', '봉', '알', '미', 'Ts', '인', '장', ' 길이로 자른', '줄', '조각', '팩', '줌', '모', '근', '캔', '작은술', '큰술', '국자', 'c', 't', '달걀', '크기', '공기']
    useless_word1 = ['발효액', '넣은 물', '블록', '남은거', '등 곁들여먹을 야채', '긴 거', '회처럼 먹는 ', '회처럼먹는', '매운', '커버쳐', '부침용','부침', '가루', '합쳐서', '냉동', '냉장', '삶은', '다진', '썬것', '검은', '슬라이스', '덧바를', '덧가루', '데운', '데진', '데쳐서 물기 짠', '데친', '더비비고', '깐것', '더건강한자연재료그릴', '더건강한', '더건강한그릴', '더건강한브런치', 'HACCP', '인증', '제품', '구운', 'Hunt', 'CJ', '완숙', '부산', '부순']
    useless_word2 = ['작은것', '100가루', '오뚜기3일숙성', '100햇', '볶음탕용', '볶음','볶음용', '부찌', '황색 고운', '황금', '황', '티백', 'plus', '믹스', '적당량', 'or원하는소스', '부리타', '겉잎', '볶은', '원액', '시럽118', '2길이로 자른 ', '차가운것', '따뜻한것', '차가운', '뜨거운', '약 16 그릇', '약5x5', '실제 소모는', '백설', '프레시안', '국산', '제일제면소', ' 몽과 1', '목우촌', '주부9단', ' 500원 크기', '5x', '5x5정도', '물3차', '부드러운', '부드럽게', '물2차', '물1차', '500원', '10x']
    useless_word = useless_word1 + useless_word2
    useless_word_at_end = ['액', '주', '청', '즙']
    uni_codes = ['\u200b', '\ufeff', 'u200b', 'ufeff']
    # ()가 있을 경우 (부터 )까지 제거
    ingredient = re.sub(r'\([^)]*\)', '', ingredient)
    # []가 있을 경우 [부터 ]까지 제거
    ingredient = re.sub(r'\[[^)]*\]', '', ingredient)
    # uni_codes 제거
    for uni_code in uni_codes:
        ingredient = ingredient.replace(uni_code, '')
    # units 제거 - 해당 단위 바로 앞에 숫자가 있을 경우에만 숫자들과 함께 제거
    for unit in units:
        ingredient = re.sub(r'(\d+)' + unit, '', ingredient)
    # useless_word 제거
    for word in useless_word:
        ingredient = ingredient.replace(word, '')
    # 특수문자 제거
    ingredient = re.sub(r'[^가-힣a-zA-Z0-9\s]', '', ingredient)
    # 공백사이에 있는 숫자 제거
    ingredient = re.sub(r'\s+(\d+)\s+', ' ', ingredient)
    ingredient = re.sub(r'^\d+', '', ingredient)
    ingredient = re.sub(r'\d+$', '', ingredient)
    # 2개이상의 공백을 1개의 공백으로 변경
    ingredient = re.sub(r'\s+', ' ', ingredient)
    # 맨 마지막에 있는 useless_word_at_end 제거
    for word in useless_word_at_end:
        ingredient = re.sub(r'.+' + word + r'$', '', ingredient)

    return ingredient.strip()

# 원본 이름과 정제된 이름 모두를 저장하기 위한 리스트
cleaned_ingredients = []

with open(file_path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        original_ingredient = row[0]
        cleaned_ingredient = clean_ingredient(original_ingredient)
        # 공백 또는 공백과 영어 또는 공백과 숫자로만 이루어진 경우 제외
        if not(re.match(r'^\s*$', cleaned_ingredient) or re.match(r'^\s*[a-zA-Z]+\s*$', cleaned_ingredient) or re.match(r'^\s*\d+\s*$', cleaned_ingredient)):
            cleaned_ingredients.append((original_ingredient, cleaned_ingredient))

# 중복 제거 및 정렬
cleaned_ingredients = list(set(cleaned_ingredients))
cleaned_ingredients.sort(key=lambda x: x[1])

with open('cleaned_ingredients_with_re.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Original Ingredient', 'Cleaned Ingredient'])  # 컬럼명 추가
    for original, cleaned in cleaned_ingredients:
        writer.writerow([original, cleaned])
