# lampy.nvim
![logo](logo.png)

Neovim remote plugin (Python3) wrapping `latex2sympy2` for symbolic LaTeX calculation.
Select LaTeX expressions and evaluate or run sympy code — all inline.

https://github.com/user-attachments/assets/ee329916-0f40-4aa2-8c3a-54263b5bab88

Inspired by [OrangeX4/Latex-Sympy-Calculator](https://github.com/OrangeX4/Latex-Sympy-Calculator).

## Installation (lazy.nvim)

```lua
{
  "SPLYASHKA/lampy.nvim",
  build = ":UpdateRemotePlugins",
  keys = {
    { "<leader>le", ":LampyEval<CR>",        mode = "x",                 ft = { "markdown", "tex" },    desc = "Lampy eval visual selection" },
    { "<leader>lE", ":LampyEvalReplace<CR>", mode = "x",                 ft = { "markdown", "tex" },    desc = "Lampy eval replace" },
    { "<leader>lf", ":LampyFactor<CR>",      mode = "x",                 ft = { "markdown", "tex" },    desc = "Lampy factor" },
    { "<leader>lx", ":LampyExpand<CR>",      mode = "x",                 ft = { "markdown", "tex" },    desc = "Lampy expand" },
    { "<leader>ld", ":LampyDefineVar<CR>",   mode = "x",                 ft = { "markdown", "tex" },    desc = "Lampy define variable" },
    { "<leader>ln", ":LampyNumerical<CR>",   mode = "x",                 ft = { "markdown", "tex" },    desc = "Lampy numerical" },
    { "<leader>lp", ":LampyPython<CR>",      mode = "x",                 ft = { "markdown", "tex" },    desc = "Lampy python" },
    { "<leader>ls", ":LampyShowVars<CR>",    ft = { "markdown", "tex" }, desc = "Lampy show variables" },
    { "<leader>lR", ":LampyResetVars<CR>",   ft = { "markdown", "tex" }, desc = "Lampy reset variables" },
  },
}
```

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
## License

MIT
