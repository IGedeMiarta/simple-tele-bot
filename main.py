import telebot
import time
import json

TOKEN = '6359169548:AAHNWHws0x38VVyyeY0t-HyAAZkvVKjKqPc'
JSON_FILE = 'data.json'  # JSON file to store the links
DONE_JSON = 'done.json'  # JSON file to store the done links

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def handle_start(message):
    guide = "Hello, welcome to the AyuSastranii bot! Here are the available commands:\n\n" \
            "/link - Save a link\n" \
            "/phone - Save a phone number\n" \
            "/check - Check the ban status\n\n" \
            "Please use the bot responsibly."
    bot.reply_to(message, guide)


@bot.message_handler(commands=['link'])
def handle_link_command(message):
    command_parts = message.text.split(' ')
    if len(command_parts) == 2:
        link = command_parts[1]
        if link_exists(link):
            bot.reply_to(message, "Link already saved.")
        else:
            save_data(link=link)
            bot.reply_to(message, "Link saved successfully!")
    else:
        bot.reply_to(message, "Please provide a link after the command.")


@bot.message_handler(commands=['phone'])
def handle_phone_command(message):
    command_parts = message.text.split(' ')
    if len(command_parts) == 2:
        phone = command_parts[1]
        if phone_exists(phone):
            bot.reply_to(message, "Phone number already saved.")
        else:
            save_data(phone=phone)
            bot.reply_to(message, "Phone number saved successfully!")
    else:
        bot.reply_to(
            message, "Please provide a phone number after the command.")


@bot.message_handler(commands=['done'])
def handle_done_command(message):
    command_parts = message.text.split(' ')
    if len(command_parts) == 2:
        link = command_parts[1]
        if done_link_exists(link):
            bot.reply_to(message, "Link is already marked as done.")
        else:
            save_done_link(link)
            bot.reply_to(message, "Link marked as done successfully!")
    else:
        bot.reply_to(message, "Please provide a link after the command.")


def save_data(link=None, phone=None):
    data = load_data()
    if not data:
        data = {}
    if link:
        if 'link' not in data:
            data['link'] = []
        data['link'].append(link)
    if phone:
        if 'phone' not in data:
            data['phone'] = []
        data['phone'].append(phone)
    save_data_to_file(data)


def load_data():
    try:
        with open(JSON_FILE, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        data = {}
    return data


def save_data_to_file(data):
    with open(JSON_FILE, 'w') as file:
        json.dump(data, file)


def link_exists(link):
    data = load_data()
    if 'link' in data:
        return link in data['link']
    return False


def phone_exists(phone):
    data = load_data()
    if 'phone' in data:
        return phone in data['phone']
    return False


def done_link_exists(link):
    done_links = load_done_links()
    return link in done_links


def save_done_link(link):
    done_links = load_done_links()
    done_links.append(link)
    save_done_links(done_links)


def load_done_links():
    try:
        with open(DONE_JSON, 'r') as file:
            done_links = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        done_links = []
    return done_links


def save_done_links(done_links):
    with open(DONE_JSON, 'w') as file:
        json.dump(done_links, file)


@bot.message_handler(commands=['check'])
def handle_check_command(message):
    messages = []
    data = load_data()
    done_links = load_done_links()
    if data:
        if 'phone' in data:
            for phone in data['phone']:
                messages.append(f"Phone: {phone} - [UNDER CHECKING..]")
        if 'link' in data:
            for link in data['link']:
                if link in done_links:
                    messages.append(f"Link: {link} - [DONE]")
                else:
                    messages.append(f"Link: {link} - [UNDER CHECKING..]")
    else:
        messages.append("No data found.")

    chat_id = message.chat.id
    for msg in messages:
        bot.send_message(chat_id, msg)
        time.sleep(1)


bot.polling()
