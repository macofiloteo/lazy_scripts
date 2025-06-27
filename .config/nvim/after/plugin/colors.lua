require("moonfly").custom_colors({
    bg = "none",
})

vim.cmd [[colorscheme moonfly]]
vim.api.nvim_set_hl(0, "Normal", { bg = "none" })
vim.api.nvim_set_hl(0, "NormalFloat", { bg = "none" })
