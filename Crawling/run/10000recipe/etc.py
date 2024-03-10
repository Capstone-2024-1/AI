from Crawling.Crawler import Crawler_10000recipe
from Crawling.Node import TreeManager

# 소고기 돼지고기 닭고기 육류 채소류 해물류 달걀/유제품 가공식품류 쌀 밀가루 건어물류 버섯류 과일류 콩/견과류 곡류 기타
crawler = Crawler_10000recipe(cartagory='기타')

tree_manager = TreeManager("10000recipe_etc", crawler)
tree_manager.build_tree()

tree_manager.save_names_to_file()
tree_manager.save_meta_data_to_file()

print("트리 구성 완료")
print(tree_manager.names)
print()
print()
print(tree_manager.meta_data)
print()
print()
print(tree_manager.timeoutlist)