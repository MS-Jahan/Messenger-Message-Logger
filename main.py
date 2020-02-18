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
        os.makedirs("message_logs/" + threadName)
    except FileExistsError:
        pass
    
    
    #os.makedirs("message_logs/" + threadName)
    
    filename = "message_logs/" + threadName + "/" + str(date.day) + "_" + str(date.month) + "_" + str(date.year)
    

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
        with open(filename, mode = w, encoding='utf8') as write_in:
            write_in.write(content + "\n")
        #write_in = open(filename, append_write)
        write_in.close()
        
    
    if USE_TELEGRAM == True:
        bot.sendMessage(bot_chat_id, "### " + threadName + " ###" + "\n" + content) 

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
    if messageObject.text == None and messageObject.sticker == None:
        for i in range(0, len(messageObject.attachments)):
            #print(messageObject.attachments[i].animated_preview_url)
            # If attachment is a temporary location.
            if hasattr(messageObject.attachments[i], 'latitude') and hasattr(messageObject.attachments[i], 'expiration_time'):
                url = "https://www.google.com/maps/place/" + str(messageObject.attachments[i].latitude) + "," + str(messageObject.attachments[i].longitude)
                t += "\nLive Location valid for " + convertSeconds(messageObject.attachment[i].expiration_time) + ": " + url
            # If attachment is just a pinned location.
            elif hasattr(messageObject.attachments[i], 'latitude') and hasattr(messageObject.attachments[i], 'longitude'):
                url = "https://www.google.com/maps/place/" + str(messageObject.attachments[i].latitude) + "," + str(messageObject.attachments[i].longitude)
                t += "\nPinned Location: " + url    
            # If gif
            elif hasattr(messageObject.attachments[i], 'animated_preview_url') and messageObject.attachments[i].animated_preview_url != None:
                #if messageObject.attachments[i].animated_preview_url != None: #If gif
                url = self.fetchImageUrl(messageObject.attachments[i].uid)
                t += "\nGif: " + url
                #t+= str(messageObject.attachments[i].animated_preview_url) + "\n\n"
                #print("Gif               " +t)
                # content = "{}: {}".format(user.name, str(messageObject.attachments[i].animated_preview_url))
                # bot.sendMessage(bot_chat_id, "### " + thread.name + " ###" + "\n" + content) 
                # writeLogs(time.ctime() + " | " + content, thread.name, date)
            # If normal image
            elif hasattr(messageObject.attachments[i], 'large_preview_url') and messageObject.attachments[i].large_preview_url != None:
                #elif messageObject.attachments[i].large_preview_url != None: #If normal image
                url = self.fetchImageUrl(messageObject.attachments[i].uid)
                t += "\nImage: " + url
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
                t += "\nVideo: " + url
    
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
        #print(str(message_object) + "\n\n\n")
        #print(message_object.attachments[0].large_preview_url)
        
        text = ''
        
        text = getMessageContent(self, text, message_object)
        content = ''
        if message_object.replied_to != None:
            reply = message_object.replied_to
            replied_to = self.fetchUserInfo(reply.author)[reply.author]
            text1 = ''
            content += "{} has replied to {}'s message, \"{}\"\nReply: {}".format(user.name, replied_to.name, getMessageContent(self, text1, reply), text)
            writeLogs(time.ctime() + " | " + content, thread.name, date)
        else:
            content += "*{}*: {}".format(user.name, text)
            #bot.sendMessage(bot_chat_id, "### " + thread.name + " ###" + "\n" + content) 
            writeLogs(time.ctime() + " | " + content, thread.name, date)
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
        #print(msg)
        content = "{} removed reaction of message * {}: {} *".format(user.name, y.name, text)
        #bot.sendMessage(bot_chat_id, "### " + thread.name + " ###" + "\n" + content) 
        writeLogs(time.ctime() + " | " + content, thread.name, date)
        
    def onColorChange( self, mid, author_id, new_color, thread_id, thread_type, ts, metadata, msg, **kwargs):
        date = datetime.now()
        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        
        content = "Conversation Theme was changed to {} by {}".format(new_color, user.name)
        writeLogs(time.ctime() + " | " + content, thread.name, date)
        
    def onEmojiChange(self, mid, author_id, new_emoji, thread_id, thread_type, ts, metadata, msg, **kwargs):  
        date = datetime.now()
        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        
        content = "Conversation Emoji was changed to {} by {}".format(new_emoji, user.name)
        writeLogs(time.ctime() + " | " + content, thread.name, date)
        
    def onTitleChange(self, mid, author_id, new_title, thread_id, thread_type, ts, metadata, msg, **kwargs):
        date = datetime.now()
        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        
        content = "Conversation Title was changed to '{}' by {}".format(new_title, user.name)
        writeLogs(time.ctime() + " | " + content, thread.name, date)
    
    def onImageChange(self, mid, author_id, new_image, thread_id, thread_type, ts, msg, **kwargs):
        date = datetime.now()
        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        url = self.fetchImageUrl(new_image)
        content = "Conversation Image was changed by {}. Link: {}".format(user.name, url)
        writeLogs(time.ctime() + " | " + content, thread.name, date)
    
    def onNicknameChange(self, mid, author_id, changed_for, new_nickname, thread_id, thread_type, ts, metadata, msg, **kwargs):
        date = datetime.now()
        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        changed_nick = self.fetchUserInfo(changed_for)[changed_for]
        content = "{} changed nickname of {} to '{}'".format(user.name, changed_nick.name, new_nickname)
        writeLogs(time.ctime() + " | " + content, thread.name, date)
    
    def onAdminAdded(self, mid, added_id, author_id, thread_id, thread_type, ts, msg, **kwargs):
        date = datetime.now()
        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        being_added = self.fetchUserInfo(added_id)[added_id]
        content = "{} added {} as an Admin.".format(user.name, being_added.name)
        writeLogs(time.ctime() + " | " + content, thread.name, date)
        
    def onAdminRemoved(self, mid, removed_id, author_id, thread_id, thread_type, ts, msg, **kwargs):
        date = datetime.now()
        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        being_removed = self.fetchUserInfo(removed_id)[removed_id]
        content = "{} removed {} as an Admin.".format(user.name, being_removed.name)
        writeLogs(time.ctime() + " | " + content, thread.name, date)
    
    def onApprovalModeChange(self, mid, approval_mode, author_id, thread_id, thread_type, ts, msg, **kwargs):    
        date = datetime.now()
        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        
        if approval_mode:
            content = "{} activated Require Admin Approval mode.".format(user.name)
        else:
            content = "{} deactivated Require Admin Approval mode.".format(user.name)
        
        writeLogs(time.ctime() + " | " + content, thread.name, date)
        
    '''def onMessageSeen(self, seen_by, thread_id, thread_type, seen_ts, ts, metadata, msg, **kwags):
        if thread_type != ThreadType.GROUP:
            if seen_by != self.uid:
                date = datetime.now()
                user = self.fetchUserInfo(seen_by)[seen_by]
                thread = self.fetchThreadInfo(thread_id)[thread_id]
                content = "Message was seen by {}".format(user.name)
                writeLogs(time.ctime() + " | " + content, thread.name, date)
                print("On message seen, metadata: " + str(metadata))'''
            
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
        
        content = "{} added {} in {}".format(user.name, ", ".join(added_member_names), thread.name)
        writeLogs(time.ctime() + " | " + content, thread.name, date)
        
    def onPersonRemoved(self, mid, removed_id, author_id, thread_id, ts, msg, **kwargs):
        date = datetime.now()
        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        being_removed = self.fetchUserInfo(removed_id)[removed_id]
        content = "{} removed {} from group.".format(user.name, being_removed.name)
        writeLogs(time.ctime() + " | " + content, thread.name, date)
        
    def onFriendRequest(self, from_id, msg, **kwargs):
        date = datetime.now()
        user = self.fetchUserInfo(from_id)[str(from_id)]
        #print(from_id)
        #print(user)
        content = "Friend request from {}".format(user.name)
        #print(content)
        threadName = 'Friend Request'
        writeLogs(time.ctime() + " | " + content, threadName, date)
        
    '''def onInbox(self, unseen, unread, recent_unread, msg, **kwargs):
        print(unseen)
        print(unread)
        print(recent_unread)
        print(msg)'''
        
    def onInbox(self, unseen, unread, recent_unread, msg, **kwargs):
        thread = self.fetchThreadList(self, limit=1, thread_location=models.ThreadLocation.PENDING)[0]
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
                content = "{}'s current typing status: {}.".format(user.name, status.name)
                writeLogs(time.ctime() + " | " + content, thread.name, date)
        
    def onGamePlayed(self, mid, author_id, game_id, game_name, score, leaderboard, thread_id, thread_type, ts, metadata, msg, **kwargs):
        date = datetime.now()
        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        print(user.name, score, game_name, leaderboard, msg) # Need rechecking *********************************
        content = "{} scored {} in {}. Leaderboard: {}".format(user.name, score, game_name, leaderboard)
        writeLogs(time.ctime() + " | " + content, thread.name, date)
        
    def onBlock(self, author_id, thread_id, thread_type, ts, msg, **kwargs):
        date = datetime.now()
        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        #print(author_id, thread_id)
        content = "{} blocked you.".format(user.name)
        writeLogs(time.ctime() + " | " + content, thread.name, date)
        
    def onUnblock(self, author_id, thread_id, thread_type, ts, msg, **kwargs):
        date = datetime.now()
        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        content = "{} unblocked you.".format(user.name)
        writeLogs(time.ctime() + " | " + content, thread.name, date)
    
    def onLiveLocation(self, mid, location, author_id, thread_id, thread_type, ts, msg, **kwargs):
        date = datetime.now()
        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        print(location)
        print(msg)
        content = "{} shared a location: {}.".format(user.name, location.url)
        writeLogs(time.ctime() + " | " + content, thread.name, date)
        
    def onCallStarted(self, mid, caller_id, is_video_call, thread_id, thread_type, ts, metadata, msg, **kwargs):
        if thread_type == ThreadType.GROUP:
            date = datetime.now()
            user = self.fetchUserInfo(caller_id)[caller_id]
            thread = self.fetchThreadInfo(thread_id)[thread_id]
            
            if is_video_call:
                content = "{} started a video call.".format(user.name)
            else:
                content = "{} started an audio call.".format(user.name)
                
            writeLogs(time.ctime() + " | " + content, thread.name, date)
        
    def onCallEnded(self, mid, caller_id, is_video_call, call_duration, thread_id, thread_type, ts, metadata, msg, **kwargs):
        if thread_type == ThreadType.GROUP:
            date = datetime.now()
            user = self.fetchUserInfo(caller_id)[caller_id]
            thread = self.fetchThreadInfo(thread_id)[thread_id]
            
            if is_video_call:
                content = "{} ended the video call. Call Duration: {}.".format(user.name, convertSeconds(call_duration))
            else:
                content = "{} ended the audio call. Call Duration: {}.".format(user.name, convertSeconds(call_duration))
                
            writeLogs(time.ctime() + " | " + content, thread.name, date)
        
    def onUserJoinedCall(self, mid, joined_id, is_video_call, thread_id, thread_type, ts, metadata, msg, **kwargs):
        if thread_type == ThreadType.GROUP:
            date = datetime.now()
            user = self.fetchUserInfo(joined_id)[joined_id]
            thread = self.fetchThreadInfo(thread_id)[thread_id]
            
            if is_video_call:
                content = "{} joined the video call.".format(user.name)
            else:
                content = "{} joined the audio call.".format(user.name)
            
            writeLogs(time.ctime() + " | " + content, thread.name, date)    
    
    def onPollCreated(self, mid, poll, author_id, thread_id, thread_type, ts, metadata, msg, **kwargs):
        date = datetime.now()
        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        content = "{} has created a poll named '{}' containg {} options: {}.".format(user.name, poll.title, poll.options_count, poll.options)
        writeLogs(time.ctime() + " | " + content, thread.name, date)
        
    def onPollVoted(self, mid, poll, added_options, removed_options, author_id, thread_id, thread_type, ts, metadata, msg, **kwargs):
        date = datetime.now()
        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        content = "{} has voted on the poll '{}' containg {} options: {}.\nAdded Options: {}.\nRemoved Options: {}.".format(user.name, poll.title, poll.options_count, poll.options, added_options, removed_options)
        writeLogs(time.ctime() + " | " + content, thread.name, date)
    
    def onPlanCreated(self, mid, plan, author_id, thread_id, thread_type, ts, metadata, msg, **kwargs):
        date = datetime.now()
        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        content = "{} has created a plan named '{}'. \nPlan Details: {}.".format(user.name, plan.name, plan)
        writeLogs(time.ctime() + " | " + content, thread.name, date) # Checking Needed ***********************

    def onPlanEnded(self, mid, plan, thread_id, thread_type, ts, metadata, msg, **kwargs):
        date = datetime.now()
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        content = "Plan '{}' was ended. \nPlan Details: {}.".format(plan.title, plan)
        writeLogs(time.ctime() + " | " + content, thread.name, date) # Checking Needed ***********************
        
    def onPlanEdited(self, mid, plan, author_id, thread_id, thread_type, ts, metadata, msg, **kwargs):
        date = datetime.now()
        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        content = "Plan '{}' was edited by {}. \nPlan Details: {}.".format(plan.title, user.name, plan)
        writeLogs(time.ctime() + " | " + content, thread.name, date) # Checking Needed ***********************
        
    def onPlanDeleted(self, mid, plan, author_id, thread_id, thread_type, ts, metadata, msg, **kwargs):
        date = datetime.now()
        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        content = "Plan '{}' was deleted by {}. \nPlan Details: {}.".format(plan.title, user.name, plan)
        writeLogs(time.ctime() + " | " + content, thread.name, date) # Checking Needed ***********************
        
    def onPlanParticipation(self, mid, plan, take_part, author_id, thread_id, thread_type, ts, metadata, msg, **kwargs):
        date = datetime.now()
        user = self.fetchUserInfo(author_id)[author_id]
        thread = self.fetchThreadInfo(thread_id)[thread_id]
        if take_part:
            content = "{} agreed to take part in the plan '{}'.".format(user.name, plan.title)
        else:
            content = "{} disagreed to take part in the plan '{}'.".format(user.name, plan.title)
        
        writeLogs(time.ctime() + " | " + content, thread.name, date) # Checking Needed ***********************


cookies = {}
try:
    # Load the session cookies
    with open('session.json', 'r') as f:
        cookies = json.load(f)
except:
    # If it fails, never mind, we'll just login again
    pass

client = CustomClient(email, password, session_cookies=cookies)
with open('session.json', 'w') as f:
    json.dump(client.getSession(), f)




print("\nProgram Started!\n")
client.listen()
