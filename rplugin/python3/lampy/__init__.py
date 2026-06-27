import pynvim

from .engine import evaluate, factor_latex, expand_latex


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
        lines = self.nvim.funcs.nvim_buf_get_lines(0, r1, r2 + 1, False)
        if len(lines) == 1:
            line = lines[0]
            self.nvim.funcs.setline(r1 + 1, line[:c1] + text + line[c2:])
        else:
            result = [lines[0][:c1] + text] + lines[1:-1] + [lines[-1][c2:]]
            self.nvim.funcs.setline(r1 + 1, result)
            if len(result) < r2 - r1 + 1:
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
