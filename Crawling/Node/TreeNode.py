from anytree import Node, RenderTree
from anytree.exporter import DotExporter
import os


class TreeNode(Node):
    def __init__(self, name, href, parent=None, meta_data=None):
        super().__init__(name, parent)
        self.href = href
        self.meta_data = meta_data
