import os
import time
from datetime import datetime
import traceback
import json
from fbchat import Client
from fbchat.models import *


email = 'randomemail1@yahoo.com' #Facebook Email
password = 'zxxcqwer1234zx' #Facebook Password
USE_TELEGRAM = True #Change to False if you don't want to use Telegram

if USE_TELEGRAM == True:
    import telepot 
    bot = telepot.Bot('00000000:45h5t78574t45h7485th7857h45y45t78h45t') # Telegram Bot Token 
    bot_chat_id = '111111111' # Your Telegram Chat ID. It can be a user's chat ID or a group's chat ID. 
    

def writeLogs(content, threadName, date):

    try:
        os.makedirs("message_logs/" + threadName)
    except FileExistsError:
        pass

    filename = "message_logs/" + threadName + "/" + str(date.day) + "_" + str(date.month) + "_" + str(date.year)

    if os.path.exists(filename):
        append_write = 'a' # append if already exists
        #content = "\n" + content
    else:
        append_write = 'w' # make a new file if not

    with open(filename, mode = append_write, encoding='utf8') as write_in:
        write_in.write(content)
    #write_in = open(filename, append_write)
    write_in.close()
    
    if USE_TELEGRAM == True:
        bot.sendMessage(bot_chat_id, "### " + threadName + " ###" + "\n" + content) 




def getMessageContent(self, t, messageObject):
    #if len(message_object.attachments) != 0:
    # Checking if it is gif
    if messageObject.text == None and messageObject.sticker == None:
        for i in range(0, len(messageObject.attachments)):
            #print(messageObject.attachments[i].animated_preview_url)
            #try: #If == ImageType
            if hasattr(messageObject.attachments[i], 'animated_preview_url') and messageObject.attachments[i].animated_preview_url != None:
                #if messageObject.attachments[i].animated_preview_url != None: #If gif
                url = self.fetchImageUrl(messageObject.attachments[i].uid)
                t += "\nGif: " + url
                #t+= str(messageObject.attachments[i].animated_preview_url) + "\n\n"
                #print("Gif               " +t)
                # content = "{}: {}".format(user.name, str(messageObject.attachments[i].animated_preview_url))
                # bot.sendMessage(bot_chat_id, "### " + thread.name + " ###" + "\n" + content) 
                # writeLogs(time.ctime() + " | " + content, thread.name, date)
            elif hasattr(messageObject.attachments[i], 'large_preview_url') and messageObject.attachments[i].large_preview_url != None:
                #elif messageObject.attachments[i].large_preview_url != None: #If normal image
                url = self.fetchImageUrl(messageObject.attachments[i].uid)
                t += "\nImage: " + url
                #t+= str(messageObject.attachments[i].large_preview_url) + "\n\n"
                #print("Image               " +t)
            elif hasattr(messageObject.attachments[i], 'url') and messageObject.attachments[i].url != None:
                #else: #If file rather than image (i.e. pdf, docx etc)
                #if messageObject.attachments[i].url != None:
                t += "\nFile: " + str(messageObject.attachments[i].url) + "\n\n"
                #print("File               " +t)
    
    # Checking if it is sticker (like button or usual sticker)
    elif messageObject.sticker != None:
        get_url = str(messageObject.sticker)
        index1 = get_url.find("url")
        index1 += 5
        index2 = get_url.find("', width=")
        t = "\nSticker: " + get_url[index1:index2]
        #print(get_url[index1:index2])
        #content = "{}: {}".format(user.name,t)
        #bot.sendMessage(bot_chat_id, "### " + thread.name + " ###" + "\n" + content) 
        #writeLogs(time.ctime() + " | " + content, thread.name, date)
    elif messageObject.text != None:
        t = messageObject.text
    
    return t





class CustomClient(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, ts, metadata, msg, **kwargs):
       # print(message_object.attachments)
        date = datetime.now()
        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        #print(len(message_object.attachments))
        #print("\n")
        print(str(message_object) + "\n\n\n")
        #print(message_object.attachments[0].large_preview_url)
        
        text = ''
        
        text = getMessageContent(self, text, message_object)
      
        content = "*{}*: {}".format(user.name, text)
        #bot.sendMessage(bot_chat_id, "### " + thread.name + " ###" + "\n" + content) 
        writeLogs(time.ctime() + " | " + content, thread.name, date)
        return

    def onReactionAdded(self, mid, reaction, author_id, thread_id, thread_type, ts, msg, **kwargs):
        date = datetime.now()

        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        x = self.fetchMessageInfo(mid, thread_id)
        y = self.fetchUserInfo(x.author)[x.author]
        #mess = x.text
        
        '''if mess == None or mess == "":
            mess = "%Sticker, image or link%"'''
        
        text = ''
        text = getMessageContent(self, text, x)
        
        
        content = "{} reacted {} to message * {}: {} *".format(user.name, reaction.name, y.name, text)
        #bot.sendMessage(bot_chat_id, "### " + thread.name + " ###" + "\n" + content) 
        writeLogs(time.ctime() + " | " + content, thread.name, date)
        
    def onReactionRemoved(self, mid, author_id, thread_id, thread_type, ts, msg, **kwargs):
        date = datetime.now()

        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        x = self.fetchMessageInfo(mid, thread_id)
        y = self.fetchUserInfo(x.author)[x.author]
        #mess = x.text
        
        '''if mess == None or mess == "":
            mess = "%Sticker, image or link%"'''
        text = ''
        text = getMessageContent(self, text, x)
        print(msg)
        content = "{} removed reaction of message * {}: {} *".format(user.name, y.name, text)
        #bot.sendMessage(bot_chat_id, "### " + thread.name + " ###" + "\n" + content) 
        writeLogs(time.ctime() + " | " + content, thread.name, date)
        
    def onColorChange( self, mid, author_id, new_color, thread_id, thread_type, ts, metadata, msg, **kwargs):
        date = datetime.now()
        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        
        content = "Conversation Theme changed to {} by {}".format(new_color, user.name)
        writeLogs(time.ctime() + " | " + content, thread.name, date)
        

try:
    with open("session.json") as f:
        cookies = json.load(f)
    client = fbchat.Client(USER, PASSWORD, session_cookies=cookies)
    print('Logging in using cookies...')
except:
    print('Cookies not found!')
    client = CustomClient(email, password)
    cookies = client.getSession()
    with open("session.json", "w+") as f:
        json.dump(cookies, f)
    print('Cookies saved!')

print("\nProgram Started!\n")
client.listen()
