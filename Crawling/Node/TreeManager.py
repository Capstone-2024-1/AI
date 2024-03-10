import os

from Crawling.Node.TreeNode import TreeNode
import csv


class TreeManager:
    def __init__(self, tree_name, crawler):
        self.root = None
        self.tree_name = tree_name
        self.crawler = crawler
        self.names = set()
        self.hrefs = {}
        self.meta_data = {}
        self.default_url = crawler.default_url
        self.timeoutlist = []

    def build_tree(self):
        self.root = TreeNode("root", self.default_url, parent=None)
        self.__build_tree_recursive__(self.root)

    def __build_tree_recursive__(self, current_node):
        try:
            print(f"current_node: {current_node.name}")
            node_level = 0
            if current_node.name != "root":
                node_level = self.crawler.check_node_level(current_node.href)
            children_datas = self.crawler.extract_data(node_level, current_node.name, current_node.href)
            print(children_datas)
            for children_data in children_datas:
                name, href, meta_data = children_data
                print(current_node.name, name)
                child_node = TreeNode(name, href, parent=current_node, meta_data=meta_data)
                if name not in self.names:
                    self.hrefs[name] = href
                    self.names.add(name)
                if meta_data != {}:
                    self.meta_data[name] = meta_data
                if node_level != -1:
                    self.__build_tree_recursive__(child_node)

                self.save_names_to_file()
                self.save_meta_data_to_file()
                self.save_timeoutlist_to_file()

        except Exception as e:
            self.crawler.get_new_driver()
            self.timeoutlist.append((current_node.name, current_node.href))
            self.__build_tree_recursive__(current_node)

            self.save_names_to_file()
            self.save_meta_data_to_file()
            self.save_timeoutlist_to_file()

    def save_names_to_file(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        filename = f"{current_dir}/data/names/{self.tree_name}_names.csv"
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['name', 'href'])
            for name in self.names:
                writer.writerow([name, self.hrefs[name]])
        if self.crawler.driver:
            self.crawler.driver.quit()
            self.crawler.driver = None

    def save_meta_data_to_file(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        filename = f"{current_dir}/data/meta_data/{self.tree_name}_meta_data.csv"
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            if self.names and self.meta_data:
                first_key = list(self.meta_data.keys())[0]
                if first_key in self.meta_data and isinstance(self.meta_data[first_key], dict):
                    fieldnames = ['name'] + list(self.meta_data[first_key].keys())
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    for name in self.names:
                        if name in self.meta_data:
                            row = {'name': name}
                            row.update(self.meta_data[name])
                            writer.writerow(row)
        if self.crawler.driver:
            self.crawler.driver.quit()
            self.crawler.driver = None

    def save_timeoutlist_to_file(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        filename = f"{current_dir}/data/timeoutlist/{self.tree_name}_timeoutlist.csv"
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            if self.timeoutlist:
                writer = csv.writer(file)
                writer.writerow(['name', 'href'])
                for name, href in self.timeoutlist:
                    writer.writerow([name, href])
        if self.crawler.driver:
            self.crawler.driver.quit()
            self.crawler.driver = None
