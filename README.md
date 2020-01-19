# Messenger-Message-Logger
Logs Messenger messages, logs them on local storage and sends a copy via telegram bot!

# Before Getting Started
*Enter your email, password, telegram chat ID and bot ID in the main.py file. 

# Installation & Usage
1. Install Python 3 in your machine.
2. Install <code>python3-pip</code> in your linux distro using apt or the package manager you have (not for windows).
3. Run <code>pip3 install fbchat telepot --user</code>.
4. Install git: <code>sudo apt install git</code> (for Ubuntu and Debian based. Command will differ for other distros. Not needed on Windows.)
4. Clone this repository using <code>git clone https://github.com/MS-Jahan/Messenger-Message-Logger</code>. On Windows, just download the zip file and extract it.
5. Change directory to repository folder from terminal or cmd: <code>cd Messenger-Message-Logger</code>.
6. Now run: <code>python3 main.py</code>


Logs when:
- [x] New text message received.
- [x] Someone sends images, gifs, stickers or any kind of attachment.
- [x] Someones reacts or remove reaction.
- [x] Someones changes thread (conversation) name, color/theme, emoji.
- [x] Someones chhanges nickname.
- [x] New friend request is received.
- [x] New video/audio call is started or someone joined in call in group conversation.
- [x] Someone adds or removes someone (as admin or general member) and toggle 'Require Admin Approval' in group conversation.
- [x] Someone starts or stops typing in private chat.
