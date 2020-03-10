from telebot.telebot import Bot
import subprocess
import os

subprocess.call(['timeout','-k','5','--foreground','5','docker','run','-t','jochnickel/lua','lua5.3','-e','print"Lua is ready."'])
print()

token = open('token.txt','r')
bot = Bot(token.read())
token.close()

def execLua(code):
	try:
		log = '>>starting lua\n'
		log = '%s%s'%(log,subprocess.check_output(['timeout','-k','10','--foreground','10','docker','run','-t','jochnickel/lua','lua5.3','-e',code]).decode())
		return '%s>>lua finished'%log, None
	except subprocess.CalledProcessError as e:
		errname = (124==e.returncode) and "timeout" or (1==e.returncode) and "error" or "returncode(%s)"%e.returncode
		log = '%s>>lua crashed\n%s'%(log,e.output.decode())
		return [ log, '`Lua interrupted (%s)`'%errname]


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
	output, *errmsg = execLua(code)
	bot.sendMessage(chat,output)
	if errmsg: bot.sendMessage(chat, *errmsg, markdown = True)


bot.onMessage = onMsg
bot.onUpdate = None
