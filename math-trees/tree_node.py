"""
TreeNode class for building tree data structures.
"""


class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []
    
    def add_child(self, child):
        self.children.append(child)
    
    def is_leaf(self):
        return len(self.children) == 0
    
    def __repr__(self):
        return f"TreeNode('{self.value}', children={len(self.children)})"
