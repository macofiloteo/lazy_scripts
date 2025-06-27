return {
    {
        "mason-org/mason.nvim",
        config = function()
            require("mason").setup()
        end
    },
    {
        "mason-org/mason-lspconfig.nvim",
        config = function()
            require("mason-lspconfig").setup({
                ensure_installed = {
                    "lua_ls",
                    "rust_analyzer",
                    "pyright",
                    "ts_ls",
                    "clangd"
                },
            })
        end
    },
    {
        "neovim/nvim-lspconfig",
        config = function()
            local nvim_lspconfig = require("lspconfig")
            nvim_lspconfig.lua_ls.setup({})
            nvim_lspconfig.rust_analyzer.setup({})
            nvim_lspconfig.pyright.setup({})
            nvim_lspconfig.ts_ls.setup({})
            nvim_lspconfig.clangd.setup({})
            local signs = {
                [vim.diagnostic.severity.ERROR] = " ",
                [vim.diagnostic.severity.WARN]  = " ",
                [vim.diagnostic.severity.HINT]  = "󰠠 ",
                [vim.diagnostic.severity.INFO]  = " ",
            }
            vim.diagnostic.config({
                signs = { text = signs },
                virtual_text = true,
                underline = true,
                update_in_insert = false,
            })
        end,
    }
}
