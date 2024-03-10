from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import time
from .Crawler import Crawler
import requests, json
from bs4 import BeautifulSoup


class Crawler_10000recipe(Crawler):
    def __init__(self, default_url="http://www.10000recipe.com/recipe/list.html", cartagory=None, delay=20):
        self.default_url = default_url
        self.cartagory = cartagory
        self.delay = delay
        self.driver = None
        self.get_new_driver()


    def check_node_level(self, href):  # 0: 루트노드, 1: 중간 노드, -1: 리프 노드
        url = self.__get_sub_url__(href)

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        s_category_tags = soup.find_all(class_="s_category_tag")

        if s_category_tags:
            for s_category_tag in s_category_tags:
                tag_conts = s_category_tag.find_all(class_="tag_cont")

                for tag_cont in tag_conts:
                    li_tags = tag_cont.find_all("li")

                    if li_tags:
                        return 1
            return -1
        else:
            return 0

    def extract_data(self, node_type, name="", href=""):
        if node_type == 0:
            return self.__extract_cate_list_data__(self.default_url)
        elif node_type == 1:
            return self.__extract_s_category_tag_data__(
                href, name
            )
        else:
            return self.__extract_common_sp_caption_tit_data__(
                href, name
            )

    def __get_sub_url__(self, href, base_url="https://www.10000recipe.com"):
        driver = self.driver

        if href.startswith("java"):
            driver.get("https://www.10000recipe.com/recipe/list.html")
            driver.implicitly_wait(self.delay)
            driver.execute_script(href[11:])

            time.sleep(self.delay)

            redirected_url = driver.current_url
            return redirected_url
        elif href == "https://www.10000recipe.com/recipe/list.html":
            return "https://www.10000recipe.com/recipe/list.html"
        elif href.startswith("http"):
            return href
        return base_url + href

    def __extract_cate_list_data__(self, url, category_num=2):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        cate_lists = soup.find_all(class_="cate_list")
        result = []

        for cate_list in cate_lists:
            links = cate_list.find_all('a')
            link_data = []
            for link in links:
                text = link.text
                href = link['href']
                if text == "전체":
                    continue
                meta_data = {}
                link_data.append((text, href, meta_data))
            result.append(link_data)

        tmp = result[:-1]
        category = ["종류별", "상황별", "재료별", "방법별"]
        result = []
        for i, val in enumerate(tmp):
            result.append((category[i], val))
        result = result[category_num][1]
        if hasattr(self, 'cartagory') and self.cartagory:
            for i in range(len(result)):
                if result[i][0] in self.cartagory:
                    return [result[i]]
        return result

    def __extract_s_category_tag_data__(self, href, name):
        now_url = self.__get_sub_url__(href)
        response = requests.get(now_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        s_category_tags = soup.find_all(class_="s_category_tag")
        results = []

        for s_category_tag in s_category_tags:
            links = s_category_tag.find_all('a')
            link_data = []
            for link in links:
                new_text = link.text
                new_href = link['href']
                if new_text == "전체" or new_href == href or name == new_text:
                    continue
                new_meta_data = {}
                link_data.append((new_text, new_href, new_meta_data))
            results.extend(link_data)

        for idx, (name, href, meta_data) in enumerate(results):
            if name == "전체":
                continue
            if href.startswith("http") and "cat" not in href:
                meta_data = self.__get_meta_data__(href, name)
                results[idx] = (name, href, meta_data)
        return results

    def __extract_common_sp_caption_tit_data__(self, href, name):
        url = self.__get_sub_url__(href)
        meta_data = self.__get_meta_data__(url, name)
        return [(name, "", meta_data)]

    def __get_meta_data__(self, now_url, name, max_try=2):
        index = 0
        food_name, href = self.__get_recipe_name_and_href__(now_url)
        ingredients = self.__extract_ingredients__(href)
        name_with_no_space = name.replace(" ", "")
        food_name_with_no_space = food_name.replace(" ", "")
        while (ingredients == [] or ingredients == {} or name_with_no_space not in food_name_with_no_space) and max_try > 0:
            max_try -= 1
            index += 1
            food_name, href = self.__get_recipe_name_and_href__(now_url,index)
            ingredients = self.__extract_ingredients__(href)
            food_name_with_no_space = food_name.replace(" ", "")
        if ingredients == {}:
            return {}
        else:
            return {"food_name": food_name, "ingredients": ingredients}

    def __get_recipe_name_and_href__(self, now_url, index=0):
        url = now_url + "&order=accuracy"
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(f"HTTP response error: {response.status_code}")

        soup = BeautifulSoup(response.text, 'html.parser')

        # 레시피 링크 추출
        href_elements = soup.select('.common_sp_link')
        if not href_elements or len(href_elements) <= index:
            raise IndexError("The specified index is out of range for href elements.")

        href = href_elements[index].get('href')

        # 레시피 이름 추출
        name_elements = soup.select('.common_sp_caption_tit.line2')
        if not name_elements or len(name_elements) <= index:
            raise IndexError("The specified index is out of range for food name elements.")

        food_name = name_elements[index].text
        return food_name, href

    def __extract_ingredients__(self, href):
        url = self.__get_sub_url__(href)
        try:
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            ingredient_elements = soup.select('div#divConfirmedMaterialArea li')

            ingredients = []

            for element in ingredient_elements:
                # 재료 이름만 추출 (양 정보는 무시)
                ingredient_name = element.find(text=True, recursive=False).strip()

                if ingredient_name:
                    ingredients.append(ingredient_name)

            return ingredients
        except Exception as e:
            return []

    def get_new_driver(self):
        if self.driver is not None:
            self.driver.quit()
        options = FirefoxOptions()
        self.driver = webdriver.Firefox(options=options)
        self.driver.set_page_load_timeout(15)
