local M = {}

function M.check()
  vim.health.start("lampy.nvim")

  local pyname = vim.g.python3_host_prog or "python3"
  local handle = io.popen(pyname .. " --version 2>&1")
  if not handle then
    vim.health.error("Python 3 not found", {
      info = "tried: " .. pyname,
      solution = "Install Python 3 and set g:python3_host_prog if needed",
    })
    return
  end
  local python_version = handle:read("*a"):gsub("%s+", "")
  handle:close()
  vim.health.ok("Python 3: " .. python_version)

  local checks = {
    pynvim = "Neovim Python client",
    latex2sympy2 = "LaTeX to sympy converter",
  }

  for mod, label in pairs(checks) do
    local h = io.popen(pyname .. " -c 'import " .. mod .. "' 2>&1")
    local err = h:read("*a")
    h:close()
    if err == "" then
      vim.health.ok(label .. ": installed")
    else
      vim.health.error(label .. ": not installed", {
        solution = "pip install " .. mod,
      })
    end
  end

  vim.health.info("Run :UpdateRemotePlugins and restart Neovim after any Python change")
end

return M
