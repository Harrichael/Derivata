from jinja2 import Template

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)

def generate_latex_tree(node, indent=0):
    """Generate LaTeX code for a tree using qtree syntax."""
    if not node:
        return ""
    
    # Start the node with its value
    latex = f"[.{node.value} "
    
    # Recursively process children
    for child in node.children:
        latex += generate_latex_tree(child, indent + 1)
    
    latex += "]"
    return latex

def main():
    # Create a sample tree
    root = TreeNode("Root")
    child1 = TreeNode("Child1")
    child2 = TreeNode("Child2")
    child3 = TreeNode("Child3")
    grandchild1 = TreeNode("Grandchild1")
    grandchild2 = TreeNode("Grandchild2")

    root.add_child(child1)
    root.add_child(child2)
    root.add_child(child3)
    child1.add_child(grandchild1)
    child2.add_child(grandchild2)

    # Generate LaTeX tree code
    tree_code = generate_latex_tree(root)

    # Define the Jinja2 LaTeX template
    latex_template = r"""
\documentclass{standalone}
\usepackage{tikz}
\usepackage{tikz-qtree}
\begin{document}
\begin{tikzpicture}
\Tree {{ tree_code }}
\end{tikzpicture}
\end{document}
"""
    # Render the template with the tree code
    template = Template(latex_template)
    latex_document = template.render(tree_code=tree_code)

    # Output to a .tex file
    with open("tree_output.tex", "w") as f:
        f.write(latex_document)
    
    print("LaTeX code for the tree has been written to 'tree_output.tex'.")

if __name__ == "__main__":
    main()
