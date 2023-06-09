import telebot
import datetime
import pytz
import requests

# Initialize the bot with your token
token = "YOU HERE TOKEN"
bot = telebot.TeleBot(token)

# Dictionary mapping time zones to flag emojis
flag_emojis = {
    "Africa/Cairo": "🇪🇬",
    "America/New_York": "🇺🇸",
    "Asia/Tokyo": "🇯🇵",
    # Add more time zones and their flag emojis here
}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_photo(message.chat.id, photo="https://graph.org/file/b0d3a4b00f7b8d8a2e099.jpg", caption="Use: /time <امريكا, usa>")

@bot.message_handler(commands=['time'])
def get_time_with_zones(message):
    args = message.text.split(maxsplit=1)
    if len(args) > 1:
        text = args[1].strip().lower()
        
        # Retrieve the time zone from the list of links
        time_zone = get_time_zone_from_links(text)
        
        if time_zone is not None and time_zone in flag_emojis:
            timezone_now = datetime.datetime.now(pytz.timezone(time_zone))
            time_now = timezone_now.strftime("%I:%M %p")
            flags_emoji = flag_emojis[time_zone]
            response = f'''
••••••••••••••••[{text.title()}]••••••••••••••      

• Current Time: {time_now}

• Flag: {flags_emoji}

• Time Zone: {time_zone}
            
••••••••••••••••[{text.title()}]••••••••••••••    
            '''
            bot.send_message(message.chat.id, text=response)
        else:
            bot.send_message(message.chat.id, text="Invalid time zone.")
    else:
        bot.send_message(message.chat.id, text="Please provide a time zone.")

def get_time_zone_from_links(country):
    # GitHub repository URL containing the links
    repo_url = "https://raw.githubusercontent.com/C2BoT/text_all_of_bot_telebot/master/Of_telebot_pythonTxt"

    try:
        # Send a GET request to retrieve the links file from the GitHub repository
        response = requests.get(repo_url)
        response.raise_for_status()

        # Extract the time zone based on the country
        links = response.text.strip().split('\n')
        for link in links:
            link_parts = link.split(',')
            if len(link_parts) >= 3:
                link_country = link_parts[0].strip().lower()
                link_country_translated = link_parts[1].strip().lower()
                if link_country == country or link_country_translated == country:
                    return link_parts[2].strip()
        
        return None

    except requests.exceptions.RequestException as e:
        print("Error retrieving links from GitHub:", e)
        return None

# Start the bot
bot.delete_webhook()
bot.polling()
