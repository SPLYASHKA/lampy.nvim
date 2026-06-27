import latex2sympy2 as _l2s2
from latex2sympy2 import latex2latex, latex2sympy, variances, var, set_variances
from sympy import factor, expand, apart, expand_trig, simplify
from sympy.printing.latex import latex as sympy_latex


def evaluate(latex: str) -> str:
    return latex2latex(latex)


def factor_latex(expr: str) -> str:
    return sympy_latex(factor(latex2sympy(expr).subs(variances)))


def expand_latex(expr: str) -> str:
    try:
        return sympy_latex(
            expand(apart(expand_trig(
                latex2sympy(expr).subs(variances))))
        )
    except Exception:
        return sympy_latex(
            expand(expand_trig(
                latex2sympy(expr).subs(variances)))
        )


def numerical_latex(expr: str) -> str:
    result = simplify(
        latex2sympy(expr).subs(variances).doit().doit()
    ).evalf(subs=variances)
    return sympy_latex(result)


_sympy_ns = {}
exec("from sympy import *", _sympy_ns)
exec("from sympy.abc import *", _sympy_ns)
exec("from latex2sympy2 import latex2sympy, latex2latex", _sympy_ns)
_sympy_ns["var"] = _l2s2.var
_sympy_ns["__builtins__"] = {
    "abs": abs, "all": all, "any": any, "bool": bool,
    "complex": complex, "dict": dict, "enumerate": enumerate,
    "float": float, "frozenset": frozenset,
    "int": int, "isinstance": isinstance, "issubclass": issubclass,
    "len": len, "list": list, "map": map, "max": max, "min": min,
    "oct": oct, "ord": ord, "pow": pow, "range": range,
    "repr": repr, "reversed": reversed, "round": round,
    "set": set, "slice": slice, "sorted": sorted, "str": str,
    "sum": sum, "tuple": tuple, "type": type, "zip": zip,
}


def python_latex(code: str) -> str:
    return str(eval(code, _sympy_ns))


def reset_vars():
    set_variances({})
    _sympy_ns["var"] = _l2s2.var
