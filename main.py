import os
import time
from datetime import datetime
import traceback
import json
from fbchat import Client
from fbchat.models import *
from fbchat import FBchatException, FBchatUserError
import onetimepass as otp
import string
import threading

start = time.time()
end = 0
threads = []

import fbchat
import re
fbchat._util.USER_AGENTS    = ["Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36"]
fbchat._state.FB_DTSG_REGEX = re.compile(r'"name":"fb_dtsg","value":"(.*?)"')
from config import *
    
'''
    def on_chat_message(msg):
        global tfa_code
        content_type, chat_type, chat_id = telepot.glance(msg)
        if tfa_state == 1:
            tfa_state == 0
            tfa_code = msg['text']
            print("2FA code: " + str(tfa_code))'''


# client = CustomClient(email, password, session_cookies=cookies)

def valid_file_name(filename:str):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    return ''.join(c for c in filename if c in valid_chars)

def login_logout(keepLooping=True, session_time=1*60*60):
    cookies = {}
    try:
        # Load the session cookies
        if os.path.isfile('session.json'):
            with open('session.json', 'r') as f:
                cookies = json.load(f)
    except:
        os.remove('session.json')
        # If it fails, never mind, we'll just login again
        if USE_TELEGRAM == True:
            bot.sendMessage(bot_chat_id, "### ATTENTION ###\nManual Configuration Needed!\nPlease login to VPS terminal")
        # client = CustomClient(email, password, max_tries=1)
    if((not cookies) != True):
        client = CustomClient(email, password, session_cookies=cookies, max_tries=1)
    else:
        if USE_TELEGRAM == True:
            bot.sendMessage(bot_chat_id, "Enter 2FA Code:")
        client = CustomClient(email, password, max_tries=1)
    
    with open('session.json', 'w') as f:
        json.dump(client.getSession(), f)

    print("\nProgram Started!\n")
    if USE_TELEGRAM == True:
        bot.sendMessage(bot_chat_id, "Program Started/Restarted!")

    client.custom_listen()
    while client.listening and client.doOneListen():
        global end, start
        end = time.time()
        if (end - start) > session_time:
            client.stopListening()
            time.sleep(5)
            break
    
    if keepLooping:
        start = time.time()
        login_logout(keepLooping=keepLooping, session_time=session_time)

def tg_send_message(bot_chat_id, message, disable_notification=True):
    try:
        bot.sendMessage(bot_chat_id, message, parse_mode="HTML", disable_notification=disable_notification)     
    except:
        bot.sendMessage(bot_chat_id, message, disable_notification=disable_notification) 
 
def writeLogs(content, threadName, date):
    global start

    if USE_TELEGRAM == True:
        reply = "<b><u>" + threadName + "</u></b>" + "\n" + content
        thread = threading.Thread(
            target=tg_send_message,
            args=(bot_chat_id, reply, )
        )
        thread.start()
    
    content = str(time.ctime()) + " | " + content

    '''try:
        os.makedirs("message_logs/" + threadName)
    except TypeError:
        os.makedirs("message_logs/" + 'UNTITLED') #FileExistsError **************#################
    except FileExistsError:
        None'''
    
    if type(threadName) == 'None' or threadName == None or threadName == 'None':
        #print("threadName is NONETYPE")
        threadName = "UNTITLED"
    
    try:
        os.makedirs("message_logs/" + valid_file_name(threadName))
    except FileExistsError:
        pass
    
    #os.makedirs("message_logs/" + threadName)
    filename = "message_logs/" + valid_file_name(threadName) + "/" + str(date.day) + "_" + str(date.month) + "_" + str(date.year)
    
    if os.path.exists(filename):
        append_write = 'a' # append if already exists
        #content = "\n" + content
    else:
        append_write = 'w' # make a new file if not
    try:
        with open(filename, mode = append_write, encoding='utf8') as write_in:
            write_in.write(content + "\n")
        #write_in = open(filename, append_write)
        write_in.close()
    except FileNotFoundError:
        with open(filename, mode = append_write, encoding='utf8') as write_in:
            write_in.write(content + "\n")
        #write_in = open(filename, append_write)
        write_in.close()


def convertSeconds(seconds):
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    seconds = (seconds % 3600) % 60
    formattedTime = "{} hours, {} minutes, {} seconds".format(hours, minutes, seconds)
    return formattedTime

# for text, image, gif, attachment or sticker-type messages
def getMessageContent(self, t, messageObject):
    #if len(message_object.attachments) != 0:
    print(messageObject)
    if (messageObject.text == None or messageObject.text == '') and messageObject.sticker == None:
        for i in range(0, len(messageObject.attachments)):
            #print(messageObject.attachments[i].animated_preview_url)
            # If attachment is a temporary location.
            if hasattr(messageObject.attachments[i], 'latitude') and hasattr(messageObject.attachments[i], 'expiration_time'):
                url = "https://www.google.com/maps/place/" + str(messageObject.attachments[i].latitude) + "," + str(messageObject.attachments[i].longitude)
                t += "\nLive Location valid for " + convertSeconds(messageObject.attachment[i].expiration_time) + ": " + url + "\n\n"
            # If attachment is just a pinned location.
            elif hasattr(messageObject.attachments[i], 'latitude') and hasattr(messageObject.attachments[i], 'longitude'):
                url = "https://www.google.com/maps/place/" + str(messageObject.attachments[i].latitude) + "," + str(messageObject.attachments[i].longitude)
                t += "\nPinned Location: " + url + "\n\n"
            # If gif
            elif hasattr(messageObject.attachments[i], 'animated_preview_url') and messageObject.attachments[i].animated_preview_url != None:
                #if messageObject.attachments[i].animated_preview_url != None: #If gif
                url = self.fetchImageUrl(messageObject.attachments[i].uid)
                t += "\nGif: " + url + "\n\n"
                #t+= str(messageObject.attachments[i].animated_preview_url) + "\n\n"
                #print("Gif               " +t)
                # content = "{}: {}".format(user.name, str(messageObject.attachments[i].animated_preview_url))
                # if USE_TELEGRAM == True:
                #    bot.sendMessage(bot_chat_id, "### " + thread.name + " ###" + "\n" + content) 
                # writeLogs(content, thread.name, date)
            # If normal image
            elif hasattr(messageObject.attachments[i], 'large_preview_url') and messageObject.attachments[i].large_preview_url != None:
                #elif messageObject.attachments[i].large_preview_url != None: #If normal image
                url = self.fetchImageUrl(messageObject.attachments[i].uid)
                t += "\nImage: " + url + "\n\n"
                #t+= str(messageObject.attachments[i].large_preview_url) + "\n\n"
                #print("Image               " +t)
            # If file attachment
            elif hasattr(messageObject.attachments[i], 'url') and messageObject.attachments[i].url != None:
                #else: #If file rather than image (i.e. pdf, docx etc)
                #if messageObject.attachments[i].url != None:
                t += "\nFile: " + str(messageObject.attachments[i].url) + "\n\n"
                #print("File               " +t)
            # If video
            elif hasattr(messageObject.attachments[i], 'preview_url') and messageObject.attachments[i].preview_url != None:
                url = messageObject.attachments[i].preview_url
                t += "\nVideo: " + url + "\n\n"
    
    # Checking if it is sticker (like button or usual sticker)
    elif messageObject.sticker != None:
        get_url = str(messageObject.sticker)
        index1 = get_url.find("url")
        index1 += 5
        index2 = get_url.find("', width=")
        t = "\nSticker: " + get_url[index1:index2] + "\n\n"
        #print(get_url[index1:index2])
        #content = "{}: {}".format(user.name,t)
        #if USE_TELEGRAM == True:
        #bot.sendMessage(bot_chat_id, "### " + thread.name + " ###" + "\n" + content) 
        #writeLogs(content, thread.name, date)
    elif messageObject.text != None:
        t = messageObject.text
    
    return t

class CustomClient(Client):

    def on2FACode(self):
        # global tfaCode
        # global tfa_code
        # try:
        #     temp = int(tfaCode)
        # except:
        #     tfaCode = 0
        if USE_TELEGRAM == True:
            bot.sendMessage(bot_chat_id, "Enter Facebook 2FA Code --> 22 seconds break")
        # print('Enter Facebook 2FA Code-1234: ')
        # while tfaCode == 0:
        #     time.sleep(5)
        time.sleep(2)
        temp = "0000"
        while(len(str(temp)) < 6):
            print(temp)
            temp = otp.get_totp(otp_key)
            time.sleep(5)
        # temp = tfaCode
        # tfaCode = 0
        print(temp)
        return temp

    def onMessage(self, author_id, message_object, thread_id, thread_type, ts, metadata, msg, **kwargs):
       # print(message_object.attachments)
        date = datetime.now()
        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        #print(len(message_object.attachments))
        #print("\n")
        #print(str(message_object) + "\n\n\n")
        #print(message_object.attachments[0].large_preview_url)
        text = ''
        text = getMessageContent(self, text, message_object)
        content = ''
        if message_object.replied_to != None:
            reply = message_object.replied_to
            replied_to = self.fetchUserInfo(reply.author)[reply.author]
            text1 = ''
            content += "<b>{}</b> has replied to <b>{}</b>'s message, <i>{}</i>\n<b>Reply</b>: {}".format(user.name, replied_to.name, getMessageContent(self, text1, reply), text)
            writeLogs(content, thread.name, date)
        else:
            content += "<b>{}</b>: {}".format(user.name, text)
            #bot.sendMessage(bot_chat_id, "### " + thread.name + " ###" + "\n" + content) 
            writeLogs(content, thread.name, date)
            #print("### " + thread.name + " ###" + "\n" + content)
        
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
        content = "<b>{}</b> reacted <i>{}</i> to message\n  <b>{}</b>: <i>{}</i> ".format(user.name, reaction, y.name, text)
        #bot.sendMessage(bot_chat_id, "### " + thread.name + " ###" + "\n" + content) 
        writeLogs(content, thread.name, date)
        
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
        #print(msg)
        content = "<b>{}</b> removed reaction of message\n  <b>{}</b>: <i>{}</i> ".format(user.name, y.name, text)
        #bot.sendMessage(bot_chat_id, "### " + thread.name + " ###" + "\n" + content) 
        writeLogs(content, thread.name, date)
        
    def onColorChange( self, mid, author_id, new_color, thread_id, thread_type, ts, metadata, msg, **kwargs):
        date = datetime.now()
        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        content = "Conversation Theme was changed to <i>{}</i> by <b>{}</b>".format(new_color, user.name)
        writeLogs(content, thread.name, date)
        
    def onEmojiChange(self, mid, author_id, new_emoji, thread_id, thread_type, ts, metadata, msg, **kwargs):  
        date = datetime.now()
        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        content = "Conversation Emoji was changed to <i>{}</i> by <b>{}</b>".format(new_emoji, user.name)
        writeLogs(content, thread.name, date)
        
    def onTitleChange(self, mid, author_id, new_title, thread_id, thread_type, ts, metadata, msg, **kwargs):
        date = datetime.now()
        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        content = "Conversation Title was changed to <i>{}</i> by <b>{}</b>".format(new_title, user.name)
        writeLogs(content, thread.name, date)
    
    def onImageChange(self, mid, author_id, new_image, thread_id, thread_type, ts, msg, **kwargs):
        date = datetime.now()
        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        url = self.fetchImageUrl(new_image)
        content = "Conversation Image was changed by <b>{}</b>. Link: {}".format(user.name, url)
        writeLogs(content, thread.name, date)
    
    def onNicknameChange(self, mid, author_id, changed_for, new_nickname, thread_id, thread_type, ts, metadata, msg, **kwargs):
        date = datetime.now()
        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        changed_nick = self.fetchUserInfo(changed_for)[changed_for]
        content = " <b>{}</b> changed nickname of <b>{}</b> to <b><u>{}</u></b>".format(user.name, changed_nick.name, new_nickname)
        writeLogs(content, thread.name, date)
    
    def onAdminAdded(self, mid, added_id, author_id, thread_id, thread_type, ts, msg, **kwargs):
        date = datetime.now()
        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        being_added = self.fetchUserInfo(added_id)[added_id]
        content = "<b>{}</b> added <b>{}</b> as an Admin.".format(user.name, being_added.name)
        writeLogs(content, thread.name, date)
        
    def onAdminRemoved(self, mid, removed_id, author_id, thread_id, thread_type, ts, msg, **kwargs):
        date = datetime.now()
        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        being_removed = self.fetchUserInfo(removed_id)[removed_id]
        content = "<b>{}</b> removed <b>{}</b> as an Admin.".format(user.name, being_removed.name)
        writeLogs(content, thread.name, date)
    
    def onApprovalModeChange(self, mid, approval_mode, author_id, thread_id, thread_type, ts, msg, **kwargs):    
        date = datetime.now()
        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        
        if approval_mode:
            content = "<b>{}</b> activated Require Admin Approval mode.".format(user.name)
        else:
            content = "<b>{}</b> deactivated Require Admin Approval mode.".format(user.name)
        
        writeLogs(content, thread.name, date)
        
    def onMessageSeen(self, seen_by, thread_id, thread_type, seen_ts, ts, metadata, msg, **kwags):
        if thread_type != ThreadType.GROUP:
            if seen_by != self.uid:
                date = datetime.now()
                user = self.fetchUserInfo(seen_by)[seen_by]
                thread = self.fetchThreadInfo(thread_id)[thread_id]
                content = "Message was seen by <b>{}</b>".format(user.name)
                writeLogs(content, thread.name, date)
                print("On message seen, metadata: " + str(metadata))
            
    def onPeopleAdded(self, mid, added_ids, author_id, thread_id, ts, msg):
        date = datetime.now()
        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        #print("\n", added_ids, "\n\n")
        added_member_names = []
        for x in range(len(added_ids)):
            user0 = self.fetchUserInfo(added_ids[x])[added_ids[x]]
            user0 = user0.name
            added_member_names.append(user0)
            
        content = "<b>{}</b> added <b>{}</b> in <b>{}</b>".format(user.name, ", ".join(added_member_names), thread.name)
        writeLogs(content, thread.name, date)
        
    def onPersonRemoved(self, mid, removed_id, author_id, thread_id, ts, msg, **kwargs):
        date = datetime.now()
        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        being_removed = self.fetchUserInfo(removed_id)[removed_id]
        content = "<b>{}</b> removed <b>{}</b> from group.".format(user.name, being_removed.name)
        writeLogs(content, thread.name, date)
        
    def onFriendRequest(self, from_id, msg, **kwargs):
        date = datetime.now()
        user = self.fetchUserInfo(from_id)[str(from_id)]
        #print(from_id)
        #print(user)
        content = "Friend request from <b>{}</b>".format(user.name)
        #print(content)
        threadName = 'Friend Request'
        writeLogs(content, threadName, date)
        
    '''def onInbox(self, unseen, unread, recent_unread, msg, **kwargs):
        print(unseen)
        print(unread)
        print(recent_unread)
        print(msg)'''
        
    def onInbox(self, unseen, unread, recent_unread, msg, **kwargs):
        thread = self.fetchThreadList(self, limit=1, thread_location=ThreadLocation.PENDING)[0]
        msg = self.fetchThreadMessages(thread_id=thread.uid, limit=1)[0]
        #print(thread, msg)
        if not msg.is_read:
            self.onMessage(author_id=msg.author, message_object=msg, thread_id=thread.uid, thread_type=thread.type)    
        
    def onTyping(self, author_id, status, thread_id, thread_type, msg, **kwargs):
        if thread_type != ThreadType.GROUP:
            if author_id != self.uid:
                date = datetime.now()
                user = self.fetchUserInfo(author_id)[author_id]
                thread = self.fetchThreadInfo(thread_id)[thread_id]
                print(status)
                content = "<b>{}</b>'s current typing status: <i>{}</i>.".format(user.name, status.name)
                writeLogs(content, thread.name, date)
        
    def onGamePlayed(self, mid, author_id, game_id, game_name, score, leaderboard, thread_id, thread_type, ts, metadata, msg, **kwargs):
        date = datetime.now()
        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        print(user.name, score, game_name, leaderboard, msg) # Need rechecking *********************************
        content = "<b>{}</b> scored <b>{}</b> in <b>{}</b>. Leaderboard: {}".format(user.name, score, game_name, leaderboard)
        writeLogs(content, thread.name, date)
        
    def onBlock(self, author_id, thread_id, thread_type, ts, msg, **kwargs):
        date = datetime.now()
        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        #print(author_id, thread_id)
        content = "<b>{}</b> blocked you.".format(user.name)
        writeLogs(content, thread.name, date)
        
    def onUnblock(self, author_id, thread_id, thread_type, ts, msg, **kwargs):
        date = datetime.now()
        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        content = "<b>{}</b> unblocked you.".format(user.name)
        writeLogs(content, thread.name, date)
    
    def onLiveLocation(self, mid, location, author_id, thread_id, thread_type, ts, msg, **kwargs):
        date = datetime.now()
        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        print(location)
        print(msg)
        content = "<b>{}</b> shared a location: {}.".format(user.name, location.url)
        writeLogs(content, thread.name, date)
        
    def onCallStarted(self, mid, caller_id, is_video_call, thread_id, thread_type, ts, metadata, msg, **kwargs):
        if thread_type == ThreadType.GROUP:
            date = datetime.now()
            user = self.fetchUserInfo(caller_id)[caller_id]
            thread = self.fetchThreadInfo(thread_id)[thread_id]
            
            if is_video_call:
                content = "<b>{}</b> started a video call.".format(user.name)
            else:
                content = "<b>{}</b> started an audio call.".format(user.name)
                
            writeLogs(content, thread.name, date)
        
    def onCallEnded(self, mid, caller_id, is_video_call, call_duration, thread_id, thread_type, ts, metadata, msg, **kwargs):
        if thread_type == ThreadType.GROUP:
            date = datetime.now()
            user = self.fetchUserInfo(caller_id)[caller_id]
            thread = self.fetchThreadInfo(thread_id)[thread_id]
            
            if is_video_call:
                content = "<b>{}</b> ended the video call. Call Duration: {}.".format(user.name, convertSeconds(call_duration))
            else:
                content = "<b>{}</b> ended the audio call. Call Duration: {}.".format(user.name, convertSeconds(call_duration))
                
            writeLogs(content, thread.name, date)
        
    def onUserJoinedCall(self, mid, joined_id, is_video_call, thread_id, thread_type, ts, metadata, msg, **kwargs):
        if thread_type == ThreadType.GROUP:
            date = datetime.now()
            user = self.fetchUserInfo(joined_id)[joined_id]
            thread = self.fetchThreadInfo(thread_id)[thread_id]
            
            if is_video_call:
                content = "<b>{}</b> joined the video call.".format(user.name)
            else:
                content = "<b>{}</b> joined the audio call.".format(user.name)
            
            writeLogs(content, thread.name, date)    
    
    def onPollCreated(self, mid, poll, author_id, thread_id, thread_type, ts, metadata, msg, **kwargs):
        date = datetime.now()
        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        content = "<b>{}</b> has created a poll named <b>{}</b> containg <b>{}</b> options: {}.".format(user.name, poll.title, poll.options_count, poll.options)
        writeLogs(content, thread.name, date)
        
    def onPollVoted(self, mid, poll, added_options, removed_options, author_id, thread_id, thread_type, ts, metadata, msg, **kwargs):
        date = datetime.now()
        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        content = "<b>{}</b> has voted on the poll <b>{}</b> containg <b>{}</b> options: {}.\nAdded Options: {}.\nRemoved Options: {}.".format(user.name, poll.title, poll.options_count, poll.options, added_options, removed_options)
        writeLogs(content, thread.name, date)
    
    def onPlanCreated(self, mid, plan, author_id, thread_id, thread_type, ts, metadata, msg, **kwargs):
        date = datetime.now()
        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        content = "<b>{}</b> has created a plan named <b>{}</b>. \nPlan Details: {}.".format(user.name, plan.name, plan)
        writeLogs(content, thread.name, date) # Checking Needed ***********************

    def onPlanEnded(self, mid, plan, thread_id, thread_type, ts, metadata, msg, **kwargs):
        date = datetime.now()
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        content = "Plan <b>{}</b> was ended. \nPlan Details: {}.".format(plan.title, plan)
        writeLogs(content, thread.name, date) # Checking Needed ***********************
        
    def onPlanEdited(self, mid, plan, author_id, thread_id, thread_type, ts, metadata, msg, **kwargs):
        date = datetime.now()
        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        content = "Plan <b>{}</b> was edited by <b>{}</b>. \nPlan Details: {}.".format(plan.title, user.name, plan)
        writeLogs(content, thread.name, date) # Checking Needed ***********************
        
    def onPlanDeleted(self, mid, plan, author_id, thread_id, thread_type, ts, metadata, msg, **kwargs):
        date = datetime.now()
        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        content = "Plan <b>{}</b> was deleted by <b>{}</b>. \nPlan Details: {}.".format(plan.title, user.name, plan)
        writeLogs(content, thread.name, date) # Checking Needed ***********************
        
    def onPlanParticipation(self, mid, plan, take_part, author_id, thread_id, thread_type, ts, metadata, msg, **kwargs):
        date = datetime.now()
        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        if take_part:
            content = "<b>{}</b> agreed to take part in the plan <b>{}</b>.".format(user.name, plan.title)
        else:
            content = "<b>{}</b> disagreed to take part in the plan <b>{}</b>.".format(user.name, plan.title)
        
        writeLogs(content, thread.name, date) # Checking Needed ***********************

# MessageLoop(bot, on_chat_message).run_as_thread()

retry = 0
while retry < 5:
    try:
        login_logout()
    except:
        retry += 1
        print("Login Failed. Retrying...")
        with open("error.txt", "a+") as f:
            f.write(str(time.ctime()) + " | " + str(traceback.format_exc()))
        time.sleep(5)
        continue