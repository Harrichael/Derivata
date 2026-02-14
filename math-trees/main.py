from jinja2 import Environment, FileSystemLoader
import os
from tree_node import TreeNode
from latex_utils import compile_latex_to_pdf

def generate_latex_tree(node, indent=0):
    """Generate LaTeX code for a tree using qtree syntax (kept for reference)."""
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

    # Load templates from files
    template_dir = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(template_dir))
    
    # Render the tree structure using jinja2
    tree_tmpl = env.get_template('tree_template.j2')
    tree_code = tree_tmpl.render(root=root).strip()
    
    # Render the full LaTeX document
    doc_tmpl = env.get_template('document_template.j2')
    latex_document = doc_tmpl.render(tree_code=tree_code)

    # Output to latex_gen folder
    output_dir = os.path.join(os.path.dirname(template_dir), 'latex_gen')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'tree_output.tex')
    
    with open(output_file, "w") as f:
        f.write(latex_document)
    
    print(f"LaTeX code for the tree has been written to '{output_file}'.")
    
    # Automatically compile to PDF
    compile_latex_to_pdf(output_file)

if __name__ == "__main__":
    main()
