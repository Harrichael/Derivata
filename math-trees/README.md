# Math Trees LaTeX Generator

Generates LaTeX tree diagrams using Jinja2 templates.

## Installation

If you get a "tikz.sty not found" error, install the required LaTeX packages:

```bash
./install_latex.sh
```

Or manually:
```bash
sudo apt-get update
sudo apt-get install -y texlive-pictures texlive-latex-extra
```

## Usage

```bash
python3 main.py
cd ../gen
pdflatex tree_output.tex
```

Generated files will be in the `gen/` folder at the repository root.

## Templates

- `tree_template.j2` - Defines the tree structure using qtree syntax
- `document_template.j2` - LaTeX document wrapper with styling
