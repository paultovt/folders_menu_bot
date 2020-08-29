# -*- coding: utf-8 -*-
import os
import telebot
from telebot import types
import datetime
import sqlite3

# if you want to use socks
#telebot.apihelper.proxy = {'https': 'socks5://login:password@ip_or_domain:port'}

root_path = os.path.dirname(os.path.realpath(__file__))
logfile = root_path + '/telebot.log'
token = 'bot_token_here'
bot = telebot.TeleBot(token)

@bot.message_handler(commands = ['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    now = datetime.datetime.now()
    chat_id = message.chat.id

    markup = main_menu(1,'01.txt')
    rootdir = root_path + "/data"
    txt = "Hello, " + str(message.chat.first_name) + ".\n\n"

    try:
        f = open(root_path + "/welcome.txt",'r')
        txt += f.read()
        f.close()
    except:
        pass

    bot.send_message(message.chat.id, txt, reply_markup = markup, parse_mode = "html")

    log = open(logfile,'a')
    log.write(str(now.strftime("%d.%m.%Y %H:%M:%S")) + " " + str(message.chat.first_name) + " " + str(message.chat.last_name) + " @" + str(message.chat.username) + " (" + str(message.chat.id) + "): " + message.text + "\n")
    log.close()

@bot.message_handler(content_types = ["text"])
def get_info(message):
    now = datetime.datetime.now()
    chat_id = message.chat.id

    log = open(logfile,'a')
    log.write(str(now.strftime("%d.%m.%Y %H:%M:%S")) + " " + str(message.chat.first_name) + " " + str(message.chat.last_name) + " @" + str(message.chat.username) + " (" + str(message.chat.id) + "): " + message.text + " (text)\n")
    log.close()

@bot.callback_query_handler(func = lambda call: call.data[0:4] == 'dir@')
def dir(call):
    now = datetime.datetime.now()
    chat_id = call.from_user.id
    callback, folder_id_str, filename = call.data.split("@")
    folder_id = int(folder_id_str)
    disablePicturePreview = False

    conn = sqlite3.connect('folders.db')
    db = conn.cursor()
    sql_query = db.execute("SELECT DISTINCT folder FROM folders WHERE folder_id = " + folder_id_str).fetchone()
    conn.close()
    rootdir = root_path + "/data"
    files = [ fa for fa in os.listdir(rootdir + sql_query[0]) if os.path.isfile(os.path.join(rootdir + sql_query[0],fa)) and fa.endswith(filename)]
    markup = main_menu(folder_id, filename)

    if folder_id == 1:
        disablePicturePreview = True

    if files:
        f = open(rootdir + sql_query[0]+"/" + filename, 'r')
        txt = f.read()
        f.close()
    else:
        txt = ""

    prefix = "◻ Main menu\n"
    if folder_id > 1:
        for each in [ " ".join(i.split(" ")[1:]) for i in sql_query[0][1:].split("/") ]:
            prefix += " ▫ " + each + "\n"
        
    bot.edit_message_text(prefix + "\n" + txt, chat_id, call.message.message_id, reply_markup = markup, disable_web_page_preview = disablePicturePreview, parse_mode = "html")
    
    log = open(logfile, 'a')
    log.write(str(now.strftime("%d.%m.%Y %H:%M:%S")) + " " + str(call.from_user.first_name) + " " + str(call.from_user.last_name) + " @" + str(call.from_user.username) + " (" + str(call.from_user.id) + "): " + call.data + " (button)\n")
    log.close()

def main_menu(folder_id, filename):
    markup = types.InlineKeyboardMarkup()
    rootdir = "./data"

    conn = sqlite3.connect('folders.db')
    db = conn.cursor()
    sql_query = db.execute("SELECT DISTINCT folder FROM folders WHERE folder_id = " + str(folder_id)).fetchone()

    files = [ fa for fa in os.listdir(rootdir + sql_query[0]) if os.path.isfile(os.path.join(rootdir + sql_query[0],fa)) and fa.endswith('.txt')]
    if len(files) > 1:
        sfiles = sorted(files)
    
        row = []
        if sfiles.index(filename) > 0:
            row.append(types.InlineKeyboardButton("⬅", callback_data = "dir@" + str(folder_id) + "@" + sfiles[sfiles.index(filename) - 1]))
        else:
            row.append(types.InlineKeyboardButton(" ", callback_data = "none"))
        row.append(types.InlineKeyboardButton(str(sfiles.index(filename) + 1) + " / " + str(len(sfiles)), callback_data = "none"))
        if sfiles.index(filename) < len(sfiles)-1:
            row.append(types.InlineKeyboardButton("➡", callback_data = "dir@" + str(folder_id) + "@" + sfiles[sfiles.index(filename) + 1]))
        else:
            row.append(types.InlineKeyboardButton(" ", callback_data = "none"))
        markup.row(*row)

    sql_query = db.execute("SELECT DISTINCT folder, folder_id FROM folders WHERE root_id = " + str(folder_id)).fetchall()
    row = []
    for f in sql_query:
        try:
            icon_f = open(rootdir + f[0] + "/icon", 'r')
            icon = icon_f.read()[:-1] + " "
            icon_f.close()
        except:
            icon = " "
        folder = f[0].split("/")[-1]
        row.append(types.InlineKeyboardButton(icon + folder.partition(" ")[2:][0], callback_data = "dir@" + str(f[1]) + "@01.txt"))
        if not int((f[0].split("/")[-1]).split(" ")[0]) % 10:
            markup.row(*row)
            row = []
    if (folder_id > 1):
        sql_query = db.execute("select distinct root_id from folders where folder_id = " + str(folder_id)).fetchall()
        markup.row(*row)
        row = []
        if (sql_query[0][0] > 1):
            row.append(types.InlineKeyboardButton("1⃣ To start", callback_data = "dir@1@01.txt"))
        row.append(types.InlineKeyboardButton("↩ Back", callback_data = "dir@" + str(sql_query[0][0]) + "@01.txt"))
    markup.row(*row)
    conn.close()

    return markup


if __name__ == '__main__':

    conn = sqlite3.connect('folders.db')
    db = conn.cursor()
    db.execute("DROP TABLE IF EXISTS folders")
    db.execute("CREATE TABLE folders (folder varchar(255), folder_id bigint(20), root_id bigint(20))")
    db.execute("INSERT INTO folders (folder, folder_id, root_id) values ('/', 1, 0)")

    root_path = os.path.dirname(os.path.realpath(__file__))
    data_dir = root_path + '/data'

    s = 1
    for n in range(1, 50):
        for line in [i for i in os.popen("find " + data_dir + " -maxdepth " + str(n) + " -mindepth " + str(n) + " -type d -printf '/%P\n' | sort").read().split('\n') if i]:
            s += 1
            name = line.split('/')[-1]
            root = line[0:line.rfind('/')] if line[0:line.rfind('/')] else '/'
            db.execute("SELECT folder_id FROM folders WHERE folder = '%s'"%(root))
            root_id = db.fetchone()[0]
            db.execute("INSERT INTO folders (folder, folder_id, root_id) VALUES ('%s',%s,%s)"%(line, str(s), str(root_id)))

    conn.commit()
    conn.close()

    bot.polling(none_stop=True)
