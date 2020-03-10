from telebot.telebot import Bot
import subprocess

token = open('token.txt','r')
bot = Bot(token.read())
token.close()

def execLua(code):
	try: return [subprocess.check_output(['docker','run','-it','jochnickel/lua','lua5.3','-e',code])]
	except subprocess.CalledProcessError as e: return ['Error:',e.output.decode()]


def onMsg(update):
	if 'message' in update: msg = update['message']
	elif 'edited_message' in update: msg = update['edited_message']
	else: return
	if 'text' in msg: text = msg['text']
	else: return
	chat = msg['chat']['id']
	code = text
	if 'entities' in msg:
		ents = msg['entities']
		for e in ents:
			if 'pre'==e['type']:
				o = e['offset']
				l = e['length']
				code = text[o:(o+l)]
				break
	for answer in execLua(code):
		bot.sendMessage(chat,answer)


bot.onMessage = onMsg
bot.onUpdate = None
