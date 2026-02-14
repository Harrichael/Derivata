"""
Library for generating random arithmetic expressions using addition and subtraction.
Starts with an answer and works backwards to ensure only integers are used.
"""

import random


class ArithmeticNode:
    """Node representing an arithmetic expression."""
    
    def __init__(self, value, operator=None):
        self.value = value
        self.operator = operator  # '+' or '-' or None for leaf
        self.left = None
        self.right = None
    
    def is_leaf(self):
        return self.left is None and self.right is None
    
    def evaluate(self):
        """Recursively evaluate the expression."""
        if self.is_leaf():
            return self.value
        
        left_val = self.left.evaluate()
        right_val = self.right.evaluate()
        
        if self.operator == '+':
            return left_val + right_val
        elif self.operator == '-':
            return left_val - right_val
        else:
            raise ValueError(f"Unknown operator: {self.operator}")
    
    def to_string(self, use_parentheses=True):
        """Convert the expression to a string."""
        if self.is_leaf():
            return str(self.value)
        
        left_str = self.left.to_string(use_parentheses)
        right_str = self.right.to_string(use_parentheses)
        
        expr = f"{left_str} {self.operator} {right_str}"
        if use_parentheses and not self.is_leaf():
            expr = f"({expr})"
        return expr


def generate_arithmetic_expression(target_value, depth, min_operand=1, max_operand=20):
    """
    Generate a random arithmetic expression that evaluates to target_value.
    
    Works backwards from the target value to ensure only integers are used.
    
    Args:
        target_value: The desired result of the expression
        depth: How many levels of operations (0 = just a number, 1 = one operation, etc.)
        min_operand: Minimum value for generated operands (default: 1)
        max_operand: Maximum value for generated operands (default: 20)
    
    Returns:
        ArithmeticNode: Root node of the expression tree
    
    Examples:
        >>> expr = generate_arithmetic_expression(10, 2)
        >>> expr.evaluate()
        10
        >>> print(expr.to_string())
        ((5 + 3) + 2)
    """
    if depth == 0:
        return ArithmeticNode(target_value)
    
    # Randomly choose operation
    operator = random.choice(['+', '-'])
    
    if operator == '+':
        # For addition: target = a + b, so we pick random a, and b = target - a
        operand_a = random.randint(min_operand, max_operand)
        operand_b = target_value - operand_a
        
        # Recursively build sub-expressions
        left = generate_arithmetic_expression(operand_a, depth - 1, min_operand, max_operand)
        right = generate_arithmetic_expression(operand_b, depth - 1, min_operand, max_operand)
        
    else:  # operator == '-'
        # For subtraction: target = a - b, so we pick random b, and a = target + b
        operand_b = random.randint(min_operand, max_operand)
        operand_a = target_value + operand_b
        
        # Recursively build sub-expressions
        left = generate_arithmetic_expression(operand_a, depth - 1, min_operand, max_operand)
        right = generate_arithmetic_expression(operand_b, depth - 1, min_operand, max_operand)
    
    node = ArithmeticNode(target_value, operator)
    node.left = left
    node.right = right
    
    return node


def generate_multiple_expressions(target_value, depth, count=5, **kwargs):
    """
    Generate multiple arithmetic expressions.
    
    Args:
        target_value: The desired result of each expression
        depth: How many levels of operations
        count: Number of expressions to generate (default: 5)
        **kwargs: Additional arguments passed to generate_arithmetic_expression
    
    Returns:
        list[ArithmeticNode]: List of expression trees
    """
    return [generate_arithmetic_expression(target_value, depth, **kwargs) for _ in range(count)]


if __name__ == "__main__":
    # Example usage
    print("Generating arithmetic expressions that equal 42:\n")
    
    for depth in range(4):
        expr = generate_arithmetic_expression(42, depth)
        result = expr.evaluate()
        expr_str = expr.to_string()
        print(f"Depth {depth}: {expr_str} = {result}")
    
    print("\n" + "="*50 + "\n")
    print("Multiple expressions with depth 3:\n")
    
    expressions = generate_multiple_expressions(100, depth=3, count=5)
    for i, expr in enumerate(expressions, 1):
        print(f"{i}. {expr.to_string(use_parentheses=False)} = {expr.evaluate()}")
