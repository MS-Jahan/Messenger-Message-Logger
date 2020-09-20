# [CODE CAN HAVE BUGS (As changes made to fbchat module). USE IT IF YOU CAN DEBUG AND LET ME KNOW IF YOU CAN.]


# Messenger-Message-Logger
Logs Messenger messages, logs them on local storage and sends a copy via Telegram bot!

# Before Getting Started
*Enter your email, password, telegram chat ID and bot ID in the main.py file. 

# Installation & Usage
1. Install Python 3 in your machine.
2. Install <code>python3-pip</code> in your linux distro using apt or the package manager you have (not for Windows).
3. Run <code>pip3 install fbchat telepot --user</code>.
4. Install git: <code>sudo apt install git</code> (for Ubuntu and Debian based. Command will differ for other distros. Not needed on Windows.)
4. Clone this repository using <code>git clone https://github.com/MS-Jahan/Messenger-Message-Logger</code>. On Windows, just download the zip file and extract it.
5. Change directory to repository folder from terminal or cmd: <code>cd Messenger-Message-Logger</code>.
6. Now run: <code>python3 main.py</code>


Logs when:
- [x] New text message received (normal message or replied message).
- [x] Someone sends images, gifs, stickers or any kind of attachment.
- [x] Someones reacts or remove reaction.
- [x] Someones changes thread (conversation) name, color/theme, emoji.
- [x] Someones changes nickname.
- [x] New friend request is received.
- [x] New video/audio call is started or someone joined call in group conversation. <i>(UNTESTED)</i>
- [x] Someone adds or removes someone (as admin or general member) and toggles 'Require Admin Approval' in group conversation.
- [x] Someone starts or stops typing in private chat.
- [x] Any kind of poll or plan activity is happened. <i>(UNTESTED)</i>
