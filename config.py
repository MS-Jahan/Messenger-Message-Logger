email = '' # Facebook Email
password = "" # Facebook Password
otp_key = "" # If 2fa is enabled. Otherwise, ignore.
USE_TELEGRAM = False #Change to False if you don't want to use Telegram

if USE_TELEGRAM == True:
    import telepot 
    bot = telepot.Bot('') # Telegram Bot Token 
    bot_chat_id = '' # Your Telegram Chat ID. It can be a user's chat ID or a group's chat ID.   
