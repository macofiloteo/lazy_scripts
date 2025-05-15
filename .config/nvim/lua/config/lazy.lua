local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not (vim.uv or vim.loop).fs_stat(lazypath) then
  vim.fn.system({
    "git",
    "clone",
    "--filter=blob:none",
    "https://github.com/folke/lazy.nvim.git",
    "--branch=stable", -- latest stable release
    lazypath,
  })
end

vim.opt.rtp:prepend(lazypath)
vim.g.mapleader = " " -- the leader key is used in many keymaps,

local plugins = {
    -- plugins go here
    {"nvim-treesitter/nvim-treesitter", build = ":TSUpdate"},
    {"bluz71/vim-moonfly-colors", name = "moonfly", lazy = false, priority = 1000 }, -- color scheme
    {"nvim-telescope/telescope.nvim", tag = "0.1.8"},
    {"nvim-telescope/telescope-ui-select.nvim"},
    {"nvim-tree/nvim-web-devicons", opts = {}},
    {
	    "nvim-tree/nvim-tree.lua",
	    version = "*",
	    lazy = false,
	    dependencies = {
		    "nvim-tree/nvim-web-devicons",
	    },
    },
    {
	    "mason-org/mason.nvim",
	    "mason-org/mason-lspconfig.nvim",
	    "neovim/nvim-lspconfig",
	    "github/copilot.vim"
    },
    {"mbbill/undotree"}
}

require("lazy").setup(plugins, {})
vim.keymap.set("n", "=", [[<cmd>vertical resize +5<cr>]]) -- make the window biger vertically
vim.keymap.set("n", "-", [[<cmd>vertical resize -5<cr>]]) -- make the window smaller vertically
vim.keymap.set("n", "+", [[<cmd>horizontal resize +2<cr>]]) -- make the window bigger horizontally by pressing shift and =
vim.keymap.set("n", "_", [[<cmd>horizontal resize -2<cr>]]) -- make the window smaller horizontally by pressing shift and -
vim.opt.undofile = true



vim.api.nvim_create_autocmd('ColorScheme', {
  callback = function()
    local highlights = {
      'Normal',
      'LineNr',
      'Folded',
      'NonText',
      'SpecialKey',
      'VertSplit',
      'SignColumn',
      'EndOfBuffer',
      'TablineFill', -- this is specific to how I like my tabline to look like
    }
    for _, name in pairs(highlights) do vim.cmd.highlight(name .. ' guibg=none ctermbg=none') end 
end, 
})
