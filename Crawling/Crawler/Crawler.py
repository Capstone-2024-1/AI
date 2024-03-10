import abc

class Crawler(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def check_node_level(self, href):
        pass

    @abc.abstractmethod
    def extract_data(self, node_type, name="", href = ""):
        pass

    @abc.abstractmethod
    def get_new_driver(self):
        pass