# lampy.nvim
![logo](logo.png)

Neovim remote plugin (Python3) wrapping `latex2sympy2` for symbolic LaTeX calculation.
Select LaTeX expressions and evaluate or run sympy code — all inline.

https://github.com/user-attachments/assets/ee329916-0f40-4aa2-8c3a-54263b5bab88

Inspired by [OrangeX4/Latex-Sympy-Calculator](https://github.com/OrangeX4/Latex-Sympy-Calculator).

## Commands

All commands operate on visual selection.

| Command | Action |
|---|---|
| `LampyEval` | `selection ⟶ selection = result` |
| `LampyEvalReplace` | `selection ⟶ result` |
| `LampyFactor` | factor selection |
| `LampyExpand` | expand selection |
| `LampyDefineVar` | define `x = 5` for subsequent evals |
| `LampyShowVars` | show stored variables |
| `LampyNumerical` | numerical evaluation |
| `LampyPython` | evaluate Python/sympy code |
| `LampyResetVars` | clear stored variables |

## Requirements

```sh
pip install latex2sympy2 pynvim
```
