from telebot.telebot import Bot
import subprocess
import os

subprocess.call('docker run --rm -t jochnickel/lua timeout -s SIGKILL 5 lua5.3 -e print("Lua_is_ready.")'.split(),timeout=20)
print()

token = open('token.txt','r')
bot = Bot(token.read())
token.close()

def execLua(code):
	log = '>>starting lua\n'

	try:
		log += subprocess.check_output('docker run --rm -t jochnickel/lua timeout -s SIGKILL 10 lua5.3 -e'.split()+[code], timeout = 15, encoding = 'utf-8')
		log += '>>lua finished'
		errmsg = None
	except subprocess.CalledProcessError as e:
		errname = (124==e.returncode) and "timeout" or (1==e.returncode) and "error" or "%s"%e
		errmsg = '`Lua interrupted (%s)`'%errname
		log += e.output
		log += '>>lua crashed\n'
	except:
		errmsg = 'Unknown Error'
		log += '>>lua crashed\n'
	return log, errmsg


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
