'''
If you don't want to use Telegram,
delete or comment out lines containing "#DTA"
 Otherwise, you'll get error!

'''


from fbchat import Client
from fbchat.models import *
import os
import time
from datetime import datetime
import telepot #DTA


email = 'ajanta@gmail.com' #Facebook Email
password = 'qwerty1234567*' #Facebook Password

bot = telepot.Bot('0000000000000000:dufyfwe87y7eydy87344444444444444444444444444y') # Telegram Bot Token #DTA
bot_chat_id = '123456789' # Your Telegram Chat ID. It can be a user's chat ID or a group's chat ID. #DTA

def writeLogs(content, threadName, date):
    try:
        os.makedirs("message_logs/" + threadName)
    except FileExistsError:
        pass
    
    
    filename = "message_logs/" + threadName + "/" + str(date.day) + "_" + str(date.month) + "_" + str(date.year)

    if os.path.exists(filename):
        append_write = 'a' # append if already exists
        content = "\n" + content
    else:
        append_write = 'w' # make a new file if not
    
    
    with open(filename, mode = append_write, encoding='utf8') as write_in:
        write_in.write(content)
    
    #write_in = open(filename, append_write)
    
    write_in.close()

class CustomClient(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, ts, metadata, msg, **kwargs):
        text = message_object.text
        if message_object.text == None:
            get_url = str(message_object.sticker)
            index1 = get_url.find("url")
            index1 += 5
            index2 = get_url.find("', width=240")
            text = get_url[index1:index2]
            print(get_url[index1:index2])
        
        date = datetime.now()
        try:
            user = self.fetchUserInfo(author_id)[author_id]
            thread = self.fetchThreadInfo(thread_id)[thread_id]
            content = "{}: {}".format(user.name, text)
            bot.sendMessage(bot_chat_id, "### " + thread.name + " ###" + "\n" + content) #DTA
            writeLogs(time.ctime() + " | " + content, thread.name, date)
            return
        except:
            thread = self.fetchThreadInfo(thread_id)[thread_id]
            content = "{}: {}".format(thread.name, text)
            bot.sendMessage(bot_chat_id, "### " + thread.name + " ###" + "\n" + content) #DTA
            writeLogs(time.ctime() + " | " + content, thread.name, date)
            return
        else:
            pass
    
    def onReactionAdded(self, mid, reaction, author_id, thread_id, thread_type, ts, msg, **kwargs):
        date = datetime.now()
        
        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        x = self.fetchMessageInfo(mid, thread_id)
        y = self.fetchUserInfo(x.author)[x.author]
        mess = x.text
        if x.text == None:
            mess = "Sticker"
        content = "{} reacted {} to message ** {}: {} **".format(user.name, reaction.name, y.name, mess)
        bot.sendMessage(bot_chat_id, "### " + thread.name + " ###" + "\n" + content) #DTA
        writeLogs(time.ctime() + " | " + content, thread.name, date)

client = CustomClient(email, password)
session = client.getSession()
print("\nProgram Started!\n")
client.listen()
