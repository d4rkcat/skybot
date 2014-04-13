#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# skyb0t.py - Skype4Py bot
#  by @d4rkcat github.com/d4rkcat
#
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
#
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License at (http://www.gnu.org/licenses/) for
## more details.

try:
	import sys, os, subprocess, socket, time, Skype4Py, random, readline, re, pty, string, threading, signal
except:
	print ' [X] Import Error, please run:\nsudo apt-get install python-pip;sudo pip install Skype4Py\n'

if not subprocess.Popen(['which', 'xdotool'], stdout=subprocess.PIPE).communicate()[0] or not subprocess.Popen(['which', 'espeak'], stdout=subprocess.PIPE).communicate()[0]:
	print " [X] Dependency Error: please run:\nsudo apt-get install xdotool;sudo apt-get install espeak\n"
	exit()

sys.path.append(os.getcwd() + '/modules/')
import cleverbot

class Printer():
	def __init__(self,data):
		sys.stdout.write("\r\x1b[K"+data.__str__())
		sys.stdout.flush()

def fhelp():
	print '\n ' + redtext + 'SkyB0t' + resettext + ''' Commands:
''' + greentext + ' ls' + resettext + ''' ONLINE/OFFLINE           -   Display friends status
''' + greentext + ' chat' + resettext + ''' USER                   -   Enter into chat mode with USER
''' + greentext + ' msg' + resettext + ''' USER MESSAGE            -   Message USER with MESSAGE
''' + greentext + ' flood' + resettext + ''' USER TIMES MESSAGE    -   Flood USER TIMES with MESSAGE
''' + greentext + ' eflood' + resettext + ''' USER TIMES           -   Flood USER TIMES with random emoticons
''' + greentext + ' egroupflood' + resettext + ''' TIMES           -   Flood any group chat TIMES with random emoticons
''' + greentext + ' groupflood' + resettext + ''' TIMES MESSAGE    -   Flood any group chat TIMES with MESSAGE
''' + greentext + ' call' + resettext + ''' USER                   -   Call USER
''' + greentext + ' search' + resettext + ''' USER                 -   Search for USER
''' + greentext + ' add' + resettext + ''' USER                    -   Add USER to contacts
''' + greentext + ' send' + resettext + ''' USER                   -   Send a file to USER
''' + greentext + ' isabot' + resettext + ''' USER                 -   Check if USER is running SkyB0t
''' + greentext + ' cmdshellserver ' + resettext + ''' USER        -   Spawn a command shell and tunnel over skype to USER
''' + greentext + ' cmdshellclient ' + resettext + ''' USER        -   Connect to a command shell tunneled over skype from USER
''' + greentext + ' history' + resettext + ''' USER FILE           -   Dump chat history with USER to FILE
''' + greentext + ' voice' + resettext + ''' ON/OFF SPEED PITCH    -   On or off, speed (80-450 default: 175),  pitch (0-99 default: 50)
''' + greentext + ' callhistory' + resettext + '''                 -   Open call history in client
''' + greentext + ' contacts' + resettext + '''                    -   Open contacts in client
''' + greentext + ' info' + resettext + ''' USER                   -   Open USER profile in client
''' + greentext + ' status' + resettext + ''' STATE                -   Change your status to STATE
''' + greentext + ' tunnelserver' + resettext + ''' USER PORT      -   Serve local PORT to USER through skype tunnel
''' + greentext + ' tunnelclient' + resettext + ''' USER PORT      -   Access tunneled service of USER on local PORT
''' + greentext + ' cleverbot' + resettext + '''                   -   Get cleverbot to answer all your chat messages
''' + greentext + ' debug' + resettext + '''                       -   Show Skype API debug
''' + greentext + ' show' + resettext + '''                        -   Show the Skype client
''' + greentext + ' hide' + resettext + '''                        -   Hide the Skype client'''

def talk(words):
	if voice:
		os.system('espeak -s ' + str(speed) + ' -p ' + str(pitch) + ' "'+ str(words) + '" 2> /dev/null&')

def ls(status):
	print ''
	a, b = '', ''
	for user in s.Friends:
		if user.Handle != 'echo123':
			if user.NumberOfAuthBuddies != 0:
				a = '\tFriends: ' + str(user.NumberOfAuthBuddies)
			if user.Country or user.City:
				b = '\t' + yellowtext + user.City + '\t' + user.Country + resettext
			if user.OnlineStatus != 'OFFLINE':
				if status.lower() == 'online' or status.lower() == 'all':
					print(greentext + user.Handle + resettext + ' (' + user.FullName + ')' + '\t' + bluetext + user.OnlineStatus + resettext + a + b )
			else:
				if status.lower() == 'offline' or status.lower() == 'all':
					print(redtext + user.Handle + resettext + ' (' + user.FullName + ')' + '\t' + bluetext + user.OnlineStatus + resettext + a + b )

def OnAttach(status):
	print ' API attachment status: ' + greentext + s.Convert.AttachmentStatusToText(status) + resettext

def runcmd(cmd):
	s.SendCommand(s.Command(cmd))

def msg(user, times, message):
	cnt, m = 0, ''
	while cnt < int(times):
		cnt += 1
		m += ' '.join(message) 
		s.SendMessage(user, m)

def chat(user):
	global chatstat, chatuser
	if checkname(user):
		print greentext + ' [*] ' + resettext + 'Chatting with ' + greentext + user + resettext + '. type ' + redtext + "'exit'" + resettext + ' to go back to main menu.\n'
		cmd = ''
		chatstat, chatuser = True, user
		while True:
			try:
				cmd = raw_input('\r(' + user + ')' + greentext + ' > ' + resettext)
				if cmd == 'exit':
					chatstat = False
					print '\n\r ' + redtext + '[*] ' + resettext + 'Returned to main menu.'
					break
				else:
					c = cmd.split(' ')
					msg(user, 1, c)
			except:
				exit()
	else:
		print redtext + user + resettext + ' not found!'

def history(user, ofile):
	chats = s.Chats
	cnt = 1
	print '\r ' + bluetext + '[*] ' + resettext + 'Dumping messages for ' + greentext + user + resettext + ' to ' + greentext + ofile + resettext + ' in the background..'
	Printer(bluetext + '> ' + resettext)
	o = open(ofile.strip('\n'), 'w')
	for c in chats:
		for m in c.Messages:
			if m.FromHandle == user:
				o.write(m.Body + '\n')
		cnt += 1
	o.close()
	print '\n\r ' + greentext + '[*] ' + resettext + 'History for ' + greentext + user + resettext + ' dumped.'
	Printer(bluetext + '> ' + resettext)

def launchshell():
	cmd = '''python -c "import os,pty,socket;s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);s.bind(('', 4444));s.listen(1);(rem, addr) = s.accept();os.dup2(rem.fileno(),0);os.dup2(rem.fileno(),1);os.dup2(rem.fileno(),2);os.putenv('HISTFILE','/dev/null');pty.spawn('/bin/bash');s.close()"'''
	os.popen(cmd)

def fdebug():
	time.sleep(0.2)
	p = subprocess.Popen(['dbus-monitor', "interface=com.Skype.API.Client"])
	p.communicate()

def OnMessageStatus(Message, Status):
	if Status == 'RECEIVED':
		global body
		body, senderhandle, senderdispname = Message.Body, Message.FromHandle, Message.FromDisplayName
		fullmsg = body.strip('\n')
		c = fullmsg.split(' ')

		if clevertime:
			botresponse = cb.Ask(fullmsg).split("\x0D")[0]
			print('\r [' + time.strftime('%H:%M:%S') + '] Cleverbot: ' + greentext + botresponse + resettext)
			s.SendMessage(senderhandle, botresponse )
		else:
			if body.startswith('ping ') or body.startswith('whois ') or body.startswith('traceroute ') or body.startswith('dig '):
				iscmd = True
			else:
				iscmd = False

			if iscmd:
				if len(c) == 2:
					if cleaninput(fullmsg) == '#':
						pass
					else: 
						s.SendMessage(senderhandle, ' (cash) Processing ' + cleaninput(c[0]) + ' command..')
						if fullmsg.startswith('ping '):
							a = os.popen('ping -c 2 -s.2 ' + cleaninput(c[1]))
						else:
							a = os.popen(cleaninput(c[0]) + ' ' + cleaninput(c[1]))
					try:
						s.SendMessage(senderhandle, a.read())
						talk('command received from ' + senderhandle + ', ' + cleaninput(c[0]) + ' processing.')
					except:
						s.SendMessage(senderhandle, ' (6) illegal command! (' + fullmsg + ')')
						
				else:
					s.SendMessage(senderhandle,' (6) illegal command! (' + fullmsg + ')')

			elif fullmsg.startswith('y0? '):
				os.system('echo ' + cleaninput(c[1]) + " | md5sum | md5sum | md5sum | cut -d ' ' -f 1 > /tmp/md5sum")
				p =  open('/tmp/md5sum', 'r')
				fsum = p.read().strip('\n')
				p.close()
				s.SendMessage(senderhandle, '(6) Sup ' + fsum)

			elif fullmsg.startswith('whatis '):
				if cleaninput(c[1]) != '#':
					s.SendMessage(senderhandle, ' (cash) Finding out what ' + cleaninput(c[1]) + ' is..')
					s.SendMessage(senderhandle, '')
					os.system('''curl -s http://dictionary.reference.com/browse/''' + cleaninput(c[1]) + ''' | grep '<meta name="description" content="' | cut -d '"' -f 4 | cut -d ',' -f 2-99 | head -c -10 > /tmp/def''')
					d = open('/tmp/def', 'r')
					s.SendMessage(senderhandle, d.read())
					d.close
				else:
					s.SendMessage(senderhandle,' (6) illegal command! (' + fullmsg + ')')

			elif fullmsg.lower().startswith('wolf '):
				know = ''
				s.SendMessage(senderhandle, ' (cash) Wolf is thinking..')
				s.SendMessage(senderhandle, '')
				os.system( 'modules/wolf.sh ' + cleaninput(' '.join(c[1:]).replace('?', ''))
				with open('/tmp/wolf', 'r') as ifile:
					for line in ifile:
						know += line
					if len(know) > 1:
						s.SendMessage(senderhandle, know)
					else:
						s.SendMessage(senderhandle, ' [*] wolf does not know, please re-phrase your question.')

			elif fullmsg.startswith('(6) Sup '):
				if c[2] == checksum:
					print greentext + ' [*] ' + senderhandle + resettext + ' is a confirmed ' + redtext + 'SkyB0t.' + resettext

			else:
				if cleaninput(body) == '#':
					if iscmd:
						print('\r [' + time.strftime('%H:%M:%S') + '] ' + senderhandle + ': ' + redtext + body + resettext)
					else:
						print('\r [' + time.strftime('%H:%M:%S') + '] ' + senderhandle + ': ' + bluetext + body + resettext)
				else:
					if iscmd:
						print('\r [' + time.strftime('%H:%M:%S') + '] ' + senderhandle + ': ' + greentext + body + resettext)
					else:
						print('\r [' + time.strftime('%H:%M:%S') + '] ' + senderhandle + ': ' + bluetext + body + resettext)
				talk(fullmsg)

			if chatstat:
				Printer('(' + chatuser + ')' + greentext + ' > ' + resettext)
			else:
				Printer(bluetext + '> ' + resettext)

def cleaninput(input):
	if re.match(r'^[A-Za-z0-9. ]+$', input):
		return input
	else:
		return '#'

def checkbot(user):
	global checksum
	randstr = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(random.randint(26,60)))
	os.system('echo ' + randstr + " | md5sum | md5sum | md5sum | cut -d ' ' -f 1 > /tmp/md5chk")
	p = open('/tmp/md5chk', 'r')
	checksum = p.read().strip('\n')
	p.close()
	s.SendMessage(user, 'y0? ' + randstr)

def checkname(user):
	for f in s.Friends:
		if f.Handle == user:
			return True
			break

def ftunnel(user, port, server, channel):
	if server:
		os.popen(os.getcwd() + '/modules/' + 'skypetunnel.py -c ' + channel + ' -a 127.0.0.1:' + port + ' 2> /dev/null')
	else:
		os.popen(os.getcwd() + '/modules/' + 'skypetunnel.py -p ' + port + ' -u ' + user + ':' + channel + ' 2> /dev/null')

def complete(text, state):
	cmds  = [ 'cleverbot', 'flood ', 'groupflood ', 'egroupflood ', 'msg ', 'cmdshellserver ', 'cmdshellclient ', 'tunnelserver ', 'tunnelclient ', 'search ', 'isabot ', 'history ', 'help', 'voice ', 'chat ', 'ls', 'exit', 'call ', 'eflood ', 'online', 'offline', 'send ', 'add ', 'show', 'hide', 'info ', 'callhistory', 'contacts', 'debug', 'status ', 'away', 'invisible' ]
	for f in s.Friends:
		if f.Handle != 'echo123':
			cmds.append(f.Handle)
	for cmd in cmds:
		if cmd.startswith(text):
			if not state:
				return cmd
			else:
				state -= 1

def fexit(signum = 0, frame = 0):
	exit()

def xdo(x, y, z):
	if z:
		return subprocess.Popen(['/usr/bin/xdotool', x, y, z], stdout=subprocess.PIPE).communicate()[0]
	else:
		return subprocess.Popen(['/usr/bin/xdotool', x, y], stdout=subprocess.PIPE).communicate()[0]

def movenclick(x, y, search):
	cmd = "/usr/bin/xdotool"
	windowid = subprocess.Popen([cmd, 'search', '--name', search], stdout=subprocess.PIPE).communicate()[0]
	if windowid:
		subprocess.Popen([cmd, 'windowactivate', windowid])
		subprocess.Popen([cmd, 'windowmove', windowid, '0', '0'])
		if search == 'Skype API':
			print ' Auto authenticating..'
			subprocess.Popen([cmd, 'mousemove', str(80), str(150)], stdout=subprocess.PIPE).communicate()[0]
			subprocess.Popen([cmd, 'click', '1'], stdout=subprocess.PIPE).communicate()[0]
		subprocess.Popen([cmd, "mousemove", str(x), str(y)], stdout=subprocess.PIPE).communicate()[0]
		time.sleep(0.3)
		subprocess.Popen([cmd, 'click', '1'], stdout=subprocess.PIPE).communicate()[0]

def eflood(user, times):
	cnt, m = 0, ''
	while cnt < int(times):
		cnt += 1
		m = "".join([random.choice(emoticons) for n in xrange(random.randint(60,250))])
		s.SendMessage(user, m)

def fcmdclient():
	os.system("gnome-terminal -e 'ncat 127.0.0.1 4444' 2> /dev/null")

def menu(cmd):
	c = cmd.strip('\n').split(' ')
	jc = ' '.join(c[1:])
	if cmd.startswith('flood'):
		try:
			if checkname(c[1]):
				user, times, message = c[1], c[2], c[3:]
				msg(user, times, message)
				talk(user + ' got flooded!')
		except:
			print ' Usage: flood username times message'

	elif cmd.startswith('groupflood '):
		for gc in s.ActiveChats:
			if len(gc.Members) > 2:
				cnt, m = 0, ''
				message = c[2:]
				while cnt < int(c[1]):
					cnt += 1
					m += ' '.join(message) 
					gc.SendMessage(m)

	elif cmd.startswith('egroupflood '):
		for gc in s.ActiveChats:
			if len(gc.Members) > 2:
				cnt = 0
				while cnt < int(c[1]):
					m = "".join([random.choice(emoticons) for n in xrange(random.randint(60,250))])
					cnt += 1
					gc.SendMessage(m)
				
	elif cmd.startswith('eflood'):
		try:
			if checkname(c[1]):
				eflood(c[1], c[2])
				talk(c[1] + ' got eflooded!')
		except:
			print ' Usage: eflood username times'

	elif cmd.startswith('run '):
		print 'running (' + jc + ')'
		runcmd(jc)

	elif cmd.startswith('cleverbot'):
		global clevertime
		if not clevertime:
			clevertime = True
			print greentext + ' [*] ' + resettext + 'Cleverbot will now respond to all chat messages'
		else:
			clevertime = False
			print greentext + ' [*] ' + resettext + 'Cleverbot disabled'

	elif cmd.startswith('info '):
		runcmd('OPEN USERINFO ' + jc)
		w = xdo('search', '--name', 'Profile for ')
		xdo('windowactivate', w, '')

	elif cmd.startswith('tunnelclient '):
		t = threading.Thread(target = ftunnel, args = (c[1], c[2], False, '0'))
		t.start()
		print greentext + ' [*] ' + resettext + 'You can now access ' + c[1] + "'s tunneled port from 127.0.0.1:" + c[2]

	elif cmd.startswith('tunnelserver '):
		t = threading.Thread(target = ftunnel, args = (c[1], c[2], True, '0'))
		t.start()
		print greentext + ' [*] ' + resettext + 'Your service on port ' + c[2] + ' can now be accessed by ' + c[1]

	elif cmd.startswith('cmdshellclient '):
		if checkname(c[1]):
			t = threading.Thread(target = ftunnel, args = (c[1], "4444", False, '1'))
			t.start()
			time.sleep(0.4)
			print greentext + ' [*] ' + resettext + 'Attempting to connect to ' + greentext + c[1] + resettext + "'s cmd shell server."
			t2 = threading.Thread(target = fcmdclient)
			t2.start()
		else:
			print ' Usage: cmdshellclient username'

	elif cmd.startswith('cmdshellserver '):
		if checkname(c[1]):
			t = threading.Thread(target = ftunnel, args = (c[1], "4444", True, '1'))
			t.start()
			print greentext + ' [*] ' + resettext + 'Launching cmd shell server to ' + greentext + c[1] + resettext
			t2 = threading.Thread(target = launchshell)
			t2.start()
		else:
			print ' Usage: cmdshellserver username'

	elif cmd.startswith('callhistory'):
		runcmd('OPEN CALLHISTORY')

	elif cmd.startswith('search '):
		for user in s.SearchForUsers(c[1]):
			if user.Country or user.City:
				a = '\t' + yellowtext + user.City + '\t' + user.Country + resettext
			print(greentext + user.Handle + resettext + ' (' + user.FullName + ')' + '\t' + a )

	elif cmd.startswith('debug'):
		t = threading.Thread(target = fdebug)
		t.start()
		time.sleep(0.3)
		Printer(greentext + '[*] ' + resettext + ' Debug output turned on\n')

	elif cmd.startswith('contacts'):
		runcmd('OPEN CONTACTS')

	elif cmd.startswith('msg '):
		if checkname(c[1]):
			msg(c[1], 1, c[2:])
		else:
			print ' Usage: msg username message'

	elif cmd.startswith('ls'):
		try:
			ls(c[1])
		except:
			ls('all')

	elif cmd.startswith('isabot '):
		try:
			if checkname(c[1]):
				checkbot(c[1])
		except:
			print ' Usage: isabot username'

	elif cmd.startswith('send '):
		try:
			if checkname(c[1]):
				runcmd('OPEN FILETRANSFER ' + c[1])
			else:
				print c[1] + ' is not a valid user!'
		except:
			print ' Usage: send username'

	elif cmd.startswith('online'):
		ls('online')

	elif cmd.startswith('add '):
		try:
			s.Client.OpenAddContactDialog(c[1])
			movenclick(530, 407, "Say Hello to")
		except:
			print ' Usage: add username'

	elif cmd.startswith('offline'):
		ls('offline')

	elif cmd.startswith('exit') or cmd == 'q' or cmd == 'e':
		exit()

	elif cmd.startswith('show'):
		client.Focus()
		w = xdo('search', '--name', ' - Skype').split('\n')
		xdo('windowactivate', w[0], '')

	elif cmd.startswith('hide'):
		client.Minimize()

	elif cmd.startswith('status '):
		try:
			s.ChangeUserStatus(c[1])
		except:
			print ' Usage: status online/away/offline/invisible'

	elif cmd.startswith('call '):
		if checkname(c[1]):
			s.PlaceCall(c[1])

	elif cmd.startswith('help') or cmd == '?':
		fhelp()

	elif cmd.startswith('chat'):
		if checkname(c[1]):
			chat(c[1])

	elif cmd.startswith('voice'):
		try:
			if c[1].lower() == 'off':
				global voice
				voice = False
				print '\n\r ' + redtext + '[*] ' + resettext + 'Voice turned off.'
			else:
				speed = c[2]
				pitch = c[3]
				if int(speed) > 450 or int(pitch) > 99 or int(speed) < 80:
					print ' Usage: voice on/off speed pitch\n Maximum speed 80-450 and pitch 0-99'
				else:
					if c[1].lower() == 'on':
						voice = True
						print '\n\r ' + greentext + '[*] ' + resettext + 'Voice turned on, speed: ' + speed + ', pitch: ' + pitch + '.'
		except:
			print ' Usage: voice on/off speed pitch\n speed 80-450 and pitch 0-99'
		
	elif cmd.startswith('history'):
		try:
			if checkname(c[1]):
				t = threading.Thread(target = history, args = (c[1], c[2]))
				t.start()
		except:
			print ' Usage: history username /path/to/outfile'

	else:
		if c[0]:
			print redtext + ' Error' + resettext + ': ' + bluetext + c[0] + resettext + ' command not found, ? for help'
		else:
			pass

voice, cmd, chatstat, speed, pitch = True, '', False, 175, 50
bluetext = '\033[01;34m'
greentext = '\033[01;32m'
redtext = '\033[01;31m'
yellowtext = '\033[01;33m'	
resettext = '\033[0m'
emoticons = [':)', ':(', ':D', '(cool)', ':O', ';)', ';(', '(:|', ':|', ':*', ':P', ':$', ':^)', '|-)', '|-(', '(inlove)', ']:)', '(yn)', '(yawn)', '(puke)', '(doh)', '(angry)', '(wasntme)', '(party)', '(worry)', '(mm)', '(nerd)', ':x', '(wave)', '(facepalm)', '(devil)', '(angel)', '(envy)', '(wait)', '(hug)', '(makeup)', '(chuckle)', '(clap)', '(think)', '(bow)', '(rofl)', '(whew)', '(happy)', '(smirk)', '(nod)', '(shake)', '(waiting)', '(emo)', '(y)', '(n)', '(handshake)', '(highfive)', '(heart)', '(lalala)', '(heidy)', '(F)', '(rain)', '(sun)', '(tumbleweed)', '(music)', '(bandit)', '(tmi)', '(coffee)', '(pi)', '(cash)', '(flex)', '(^)', '(beer)', '(d)', '\o/', '(ninja)', '(*)', '(finger)', '(drunk)', '(ci)', '(toivo)', '(rock)', '(headbang)', '(bug)', '(fubar)', '(poolparty)', '(swear)', '(mooning)', '(hug)', '(kate)', '(whew)', '(punch)', '(ss)', '(u)', '(e)', '(london)', '(time)', '(~)', '(ph)' ]

readline.parse_and_bind("tab: complete")
readline.set_completer(complete)
signal.signal(signal.SIGINT, fexit)
cb=cleverbot.Session()
clevertime = False

def attach():
	s.Attach()

s = Skype4Py.Skype()
client = s.Client
s.OnAttachmentStatus = OnAttach
s.OnMessageStatus = OnMessageStatus
s.FriendlyName = "d4rkcat's^SkyB0t"
if client.IsRunning == 0 :
	client.Start()
	raw_input(bluetext + '[>] ' + resettext + 'Please authenticate to Skype then press Enter to continue.\n')

print('***************************************')
print redtext + " d4rkcat's SkyB0t Initializing.." + resettext
print ' Injecting into Skype..'

try:
	t = threading.Thread(target = attach)
	t.start()
	time.sleep(0.1)
	t2 = threading.Thread(target = movenclick, args = (270, 185, 'Skype API'))
	t2.start()

except:
	print redtext + ' Error' + resettext + ': please authenticate to skype first.'
	exit()
time.sleep(0.5)
print('***************************************')

while True:
	try:
		menu(raw_input('\r' + bluetext + '> ' + resettext))
	except:
		print ''
		exit()