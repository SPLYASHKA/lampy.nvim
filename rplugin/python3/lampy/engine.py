from latex2sympy2 import latex2latex, latex2sympy
from latex2sympy2 import latex # NOTE: may be used in the future?
from sympy import factor, expand
from sympy.printing.latex import latex as sympy_latex


def evaluate(latex: str) -> str:
    return latex2latex(latex)


def factor_latex(expr: str) -> str:
    return sympy_latex(factor(latex2sympy(expr)))


def expand_latex(expr: str) -> str:
    return sympy_latex(expand(latex2sympy(expr)))
