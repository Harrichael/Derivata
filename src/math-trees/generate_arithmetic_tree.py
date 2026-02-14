"""
Example: Generate arithmetic expressions and visualize them as LaTeX trees.
"""

from jinja2 import Environment, FileSystemLoader
import os
import sys
from arithmetic_generator import generate_arithmetic_expression
from latex_utils import compile_latex_to_pdf


def arithmetic_to_tree_node(arith_node):
    """Convert ArithmeticNode to TreeNode for visualization."""
    from tree_node import TreeNode
    
    if arith_node.is_leaf():
        return TreeNode(str(arith_node.value))
    
    # Create node with operator
    tree_node = TreeNode(arith_node.operator)
    
    # Add children
    left_child = arithmetic_to_tree_node(arith_node.left)
    right_child = arithmetic_to_tree_node(arith_node.right)
    
    tree_node.add_child(left_child)
    tree_node.add_child(right_child)
    
    return tree_node


def generate_arithmetic_tree_latex(target_value, depth, output_filename="arithmetic_tree.tex", compile_pdf=True):
    """
    Generate an arithmetic expression and create a LaTeX visualization.
    
    Args:
        target_value: The desired result
        depth: Expression depth
        output_filename: Output filename in gen folder
        compile_pdf: Whether to automatically compile to PDF (default: True)
    """
    # Generate arithmetic expression
    arith_expr = generate_arithmetic_expression(target_value, depth)
    
    print(f"Generated expression: {arith_expr.to_string(use_parentheses=False)}")
    print(f"Result: {arith_expr.evaluate()}")
    
    # Convert to tree structure
    tree_root = arithmetic_to_tree_node(arith_expr)
    
    # Load templates from templates folder
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))
    
    # Render the tree structure
    tree_tmpl = env.get_template('tree_template.j2')
    tree_code = tree_tmpl.render(root=tree_root).strip()
    
    # Render the full LaTeX document
    doc_tmpl = env.get_template('document_template.j2')
    latex_document = doc_tmpl.render(tree_code=tree_code)
    
    # Output to gen folder at repo root (navigate up from src/math-trees/ to repo root)
    script_dir = os.path.dirname(os.path.abspath(__file__))  # src/math-trees/
    src_dir = os.path.dirname(script_dir)  # src/
    repo_root = os.path.dirname(src_dir)  # Derivata/
    output_dir = os.path.join(repo_root, 'gen')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, output_filename)
    
    with open(output_file, "w") as f:
        f.write(latex_document)
    
    print(f"LaTeX tree written to '{output_file}'")
    
    # Compile to PDF if requested
    if compile_pdf:
        compile_latex_to_pdf(output_file)

