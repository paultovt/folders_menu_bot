# Telegram bot with menu created from folders.

This bot allows you to organize texts in inline menues and submenues by just creating folders and subfolders. Perfect for FAQ bot or as a informational part of multifunctional bot.

You can see the working example of this bot [here](https://t.me/folders_menu_bot).

I've done this bot to satisfy my personal needs. So you can modify it if you want more functionality. Or you can share your idea.

#### If you don't like this bot, then make your own, goddammit!

## Features

- saves all folders structure to sqlite, but can easily migrate to mysql/postgres;
- supports adding an emoji icons as prefix to name of menu;
- supports multipage texts;
- supports HTML markdown;
- if folder's prefix number % 10 == 0, then adds new row after - so you can add up to 9 buttons in one row;
- previews images from web;
- logging every users's action;
- no need to restart bot service if folders changed - just execute `update_folders.py`;
- no need to do anything if files changed only (including icons) - bot picks 'em up on the fly.

## Requirements

    python3 -m pip install -r requirements.txt
