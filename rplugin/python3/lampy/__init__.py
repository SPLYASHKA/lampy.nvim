import pynvim

from .engine import evaluate, factor_latex, expand_latex, numerical_latex, python_latex, reset_vars, latex2sympy, variances


@pynvim.plugin
class LampyPlugin:
    def __init__(self, nvim):
        self.nvim = nvim

    def _get_selection_span(self):
        funcs = self.nvim.funcs
        _, sr, sc, _ = funcs.getpos("'<")
        _, er, ec, _ = funcs.getpos("'>")
        if sr == 0 or er == 0:
            return None
        return (
            (sr - 1, min(sc, len(funcs.getline(sr))) - 1),
            (er - 1, min(ec, len(funcs.getline(er)))),
        )

    def _extract_text(self, span):
        (r1, c1), (r2, c2) = span
        lines = self.nvim.funcs.nvim_buf_get_lines(0, r1, r2 + 1, False)
        if not lines:
            return ""
        if len(lines) == 1:
            return lines[0][c1:c2]
        return "\n".join([lines[0][c1:]] + lines[1:-1] + [lines[-1][:c2]])

    def _replace_span(self, span, text):
        (r1, c1), (r2, c2) = span
        old = self.nvim.funcs.nvim_buf_get_lines(0, r1, r2 + 1, False)
        parts = text.split("\n")

        if len(parts) == 1:
            first = old[0][:c1] + parts[0] + old[-1][c2:]
            self.nvim.funcs.setline(r1 + 1, [first])
            if r2 > r1:
                self.nvim.funcs.deletebufline(0, r1 + 2, r2 + 1)
        else:
            first = old[0][:c1] + parts[0]
            last = parts[-1] + old[-1][c2:]
            result = [first] + parts[1:-1] + [last]
            self.nvim.funcs.setline(r1 + 1, result)
            excess = (r2 - r1 + 1) - len(result)
            if excess > 0:
                self.nvim.funcs.deletebufline(0, r1 + len(result) + 1, r2 + 1)

    def _transform_selection(self, transform):
        span = self._get_selection_span()
        if span is None:
            self.nvim.err_write("lampy: no selection\n")
            return
        try:
            self._replace_span(span, transform(self._extract_text(span)))
        except Exception as e:
            self.nvim.err_write(f"lampy error: {e}\n")

    @pynvim.command("LampyEval", range="", nargs="*")
    def eval_command(self, _, _range):
        self._transform_selection(lambda text: f"{text} = {evaluate(text)}")

    @pynvim.command("LampyEvalReplace", range="", nargs="*")
    def eval_replace_command(self, _, _range):
        self._transform_selection(evaluate)

    @pynvim.command("LampyFactor", range="", nargs="*")
    def factor_command(self, _, _range):
        self._transform_selection(factor_latex)

    @pynvim.command("LampyExpand", range="", nargs="*")
    def expand_command(self, _, _range):
        self._transform_selection(expand_latex)

    @pynvim.command("LampyNumerical", range="", nargs="*")
    def numerical_command(self, _, _range):
        self._transform_selection(numerical_latex)

    @pynvim.command("LampyPython", range="", nargs="*")
    def python_command(self, _, _range):
        self._transform_selection(lambda text: f"{text} = {python_latex(text)}")

    @pynvim.command("LampyDefineVar", range="", nargs="*")
    def define_var_command(self, _, _range):
        span = self._get_selection_span()
        if span is None:
            self.nvim.err_write("lampy: no selection\n")
            return
        try:
            latex2sympy(self._extract_text(span))
            self.nvim.out_write("lampy: variable defined\n")
        except Exception as e:
            self.nvim.err_write(f"lampy error: {e}\n")

    @pynvim.command("LampyShowVars", range="", nargs="*")
    def show_vars_command(self, _, _range):
        if not variances:
            self.nvim.out_write("lampy: no variables\n")
            return
        self.nvim.out_write("lampy variables:\n")
        for k, v in variances.items():
            self.nvim.out_write(f"  {k} = {v}\n")

    @pynvim.command("LampyResetVars", range="", nargs="*")
    def reset_vars_command(self, _, _range):
        reset_vars()
        self.nvim.out_write("lampy: variables cleared\n")
