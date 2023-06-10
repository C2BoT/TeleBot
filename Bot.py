import requests
import datetime
import pytz
import telebot

# Initialize the bot with your token
token = "1234567890:VfWAii_ls?***"
bot = telebot.TeleBot(token)

# GitHub repository URL containing the data
repo_url = "https://raw.githubusercontent.com/C2BoT/TeleBot/master/Of_telebot_pythonTxt"

@bot.message_handler(commands=['start'])
def handle_start_command(message):
    bot.reply_to(message, "Hey! Send the /text command followed by your country name to get information.")

@bot.message_handler(commands=['text'])
def handle_text_command(message):
    # Extract the texts after the command
    texts = message.text.split(maxsplit=1)[1].strip().split()

    try:
        # Send a GET request to retrieve the data file from the GitHub repository
        response = requests.get(repo_url)
        response.raise_for_status()

        # Extract the time zone and flag emoji information
        data_lines = response.text.strip().split('\n')

        matched_countries = []
        for line in data_lines:
            line_parts = line.split(',')
            arabic_country = line_parts[0].strip()
            english_country = line_parts[1].strip()
            time_zone = line_parts[2].strip()
            flag_emoji = line_parts[3].strip()

            for text in texts:
                if (text.lower() == english_country.lower()) or (text == arabic_country.upper()):
                    country = english_country if text.lower() == english_country.lower() else arabic_country

                    timezone_now = datetime.datetime.now(pytz.timezone(time_zone))
                    time_now = timezone_now.strftime("%I:%M %p")

                    matched_countries.append(
                        f"Country: {country}\nTime Zone: {time_zone}\nFlag: {flag_emoji}\nCurrent Time: {time_now}"
                    )
                    break

        if matched_countries:
            message_texts = "\n\n".join(matched_countries)
            bot.reply_to(message, message_texts)
        else:
            bot.reply_to(message, "Countries not found.")

    except requests.exceptions.RequestException as e:
        bot.reply_to(message, f"Error retrieving data from GitHub: {e}")

@bot.message_handler(func=lambda message: True)
def handle_text_message(message):
    bot.reply_to(message, "Invalid command. Please use the /text command.")

# Start the bot
bot.polling()
