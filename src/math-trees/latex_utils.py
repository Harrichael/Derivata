"""
Utility functions for LaTeX compilation and file operations.
"""

import os
import subprocess
import sys


def compile_latex_to_pdf(tex_file_path):
    """
    Compile a LaTeX file to PDF using pdflatex.
    
    Args:
        tex_file_path: Path to the .tex file
    
    Returns:
        bool: True if successful, False otherwise
    """
    tex_dir = os.path.dirname(tex_file_path)
    tex_filename = os.path.basename(tex_file_path)
    
    try:
        # Run pdflatex with output redirected to the same directory
        result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', '-output-directory', tex_dir, tex_filename],
            cwd=tex_dir,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            pdf_path = tex_file_path.replace('.tex', '.pdf')
            print(f"✓ PDF compiled successfully: {pdf_path}")
            return True
        else:
            print(f"✗ LaTeX compilation failed. Check the log file for details.")
            if "tikz.sty" in result.stdout or "tikz" in result.stderr:
                print("  Hint: Install LaTeX packages with: ./install_latex.sh")
            return False
    
    except FileNotFoundError:
        print("✗ pdflatex not found. Install with: sudo apt-get install texlive-latex-base")
        return False
    except subprocess.TimeoutExpired:
        print("✗ LaTeX compilation timed out")
        return False
    except Exception as e:
        print(f"✗ Error during compilation: {e}")
        return False
