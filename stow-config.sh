#!/bin/bash

DIR_NAME=$(dirname "$0")
CONFIG_PATH="$HOME"/.config
STOW_DIR_PATH="$CONFIG_PATH"/stow-config
rm -rf "$STOW_DIR_PATH"
mkdir -p "$STOW_DIR_PATH"
cp -r "$DIR_NAME"/.config/* "$STOW_DIR_PATH"/
cd "$CONFIG_PATH"
rm -rf alacritty hypr nvim tofi waybar
cd "$STOW_DIR_PATH"
stow .
hyprctl reload
