from telebot.telebot import Bot
import subprocess
import os

subprocess.call(['docker','--version'],stdout=open(os.devnull, 'wb'))
subprocess.call(['timeout','--version'],stdout=open(os.devnull, 'wb'))

token = open('token.txt','r')
bot = Bot(token.read())
token.close()

def execLua(code):
	try:
		return [subprocess.check_output(['timeout','-k','10','10','docker','run','-t','jochnickel/lua','lua5.3','-e',code])]
	except subprocess.CalledProcessError as e:
		errcode = (124==e.returncode) and "timeout" or (1==e.returncode) and "error" or "returncode(%s)"%e.returncode
		print(e.returncode,e.output)
		return [ 'Lua interrupted (%s):'%errcode , e.output.decode() ]


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
