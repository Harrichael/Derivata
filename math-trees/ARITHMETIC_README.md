# Arithmetic Expression Generator

Python library for generating random arithmetic expressions using addition and subtraction.

## Features

- **Backwards generation**: Starts with a target answer and works backwards to ensure only integers are used
- **Depth control**: Specify how many levels of operations to generate
- **Guaranteed correctness**: All expressions evaluate to the target value
- **Tree structure**: Built as a tree for easy visualization and manipulation

## Usage

### Basic Generation

```python
from arithmetic_generator import generate_arithmetic_expression

# Generate an expression that equals 42 with depth 3
expr = generate_arithmetic_expression(target_value=42, depth=3)

# Get the string representation
print(expr.to_string())  # e.g., "((5 + 3) + (20 - 6))"

# Verify it evaluates correctly
print(expr.evaluate())  # 42
```

### Generate Multiple Expressions

```python
from arithmetic_generator import generate_multiple_expressions

# Generate 5 different expressions that all equal 100
expressions = generate_multiple_expressions(100, depth=3, count=5)

for expr in expressions:
    print(f"{expr.to_string(use_parentheses=False)} = {expr.evaluate()}")
```

### Visualize as LaTeX Tree

```python
from generate_arithmetic_tree import generate_arithmetic_tree_latex

# Generate and create LaTeX visualization
generate_arithmetic_tree_latex(
    target_value=42,
    depth=2,
    output_filename="my_expression.tex"
)

# This creates latex_gen/my_expression.tex
# Compile with: cd ../latex_gen && pdflatex my_expression.tex
```

## Parameters

### `generate_arithmetic_expression(target_value, depth, min_operand=1, max_operand=20)`

- **target_value**: The desired result of the expression
- **depth**: How many levels of operations (0 = just a number, 1 = one operation, etc.)
- **min_operand**: Minimum value for generated operands (default: 1)
- **max_operand**: Maximum value for generated operands (default: 20)

## Examples

```bash
# Run the example script
python3 arithmetic_generator.py

# Generate and visualize arithmetic trees
python3 generate_arithmetic_tree.py
```

## How It Works

The generator works backwards from the target value:

1. Start with the target value
2. For each depth level:
   - Randomly choose addition or subtraction
   - For addition `target = a + b`: pick random `a`, calculate `b = target - a`
   - For subtraction `target = a - b`: pick random `b`, calculate `a = target + b`
3. Recursively apply this process to build an expression tree

This ensures all intermediate values are integers and the final result is guaranteed to equal the target.
