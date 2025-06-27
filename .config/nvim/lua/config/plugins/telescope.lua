return {
    { "nvim-telescope/telescope-ui-select.nvim" },
    {
        "nvim-telescope/telescope.nvim",
        tag = "0.1.8",
        config = function()
            require("telescope").setup({
                extensions = {
                    ["ui_select"] = { require("telescope.themes").get_dropdown }
                },
                pickers = {
                    find_files = {
                        hidden = true,
                    }
                },
                defaults = {
                    file_ignore_patterns = { ".git/", "node_modules" },
                }
            })
            require("telescope").load_extension("ui-select")
        end
    }
}
