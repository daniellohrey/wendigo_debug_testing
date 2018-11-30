import Queue
import time
import re
import xxhash
import base64
from Crypto.PublicKey import RSA

class Config:
	def __init__(self):
		self.mod = "modules/"
		self.config = "config/"
		self.data = "data/"
		self.repo = "wendigo_test"
		self.usr = "daniellohrey"
		self.token = "MmZmODE2ODZiZDBhZjc2ZTVhNDU5ZGZlZDYwOTQ0NTVlNDI2ODYxNA=="
		self.pk = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAndOV4VLdGZgIk+YcW7Kl\nVwiBiesJq6upfiRBo2hM5CEzQiSeBa1/A4h5ozSgQtSgKURVmlDChTNrs0P4bwvi\npCvq8B5SdBw4gcc7YTy03Hl11wfbIPCwqA9JwUl6ZzQtEbw7BAfndry44+2QmAoL\nU2uOoyW2C4MjmUG6SDmNfAL/PsMCvL4fiBJh2V2EUWtCPEqkVIGUHERFFaJwFea3\nFdIqIFVV4SzU6c73wdRFWKHie5WZ4GXQ3GaIAe2cyCMp3UavOhpk4s+N5xdG1xXs\n2AvfXuotYRVxvmSz+L0QiyTXNn0gmphLrMph3jyY/+KX4TH0wIxEx1ZK1gYO8D1V\npQIDAQAB\n-----END PUBLIC KEY-----"
		self.pwd = "zippass"
		self.sleep = 5
		self.fn_s = "fn_seed"
		self.id_s = "id_seed"
		self.size = 256
		self.tasks = Queue.Queue()
		self.id = self.new_id()
		self.pk = self.import_key()

	def new_id(self):
		i_time = int(time.time())
		t_id = str(i_time) + self.fixstr(self.id_s)
		self.id = str(xxhash.xxh64(t_id).hexdigest())

	def my_id(self):
		return str(xxhash.xxh64(str(self.id)).hexdigest())

	def my_mod(self):
		return self.fixstr(self.mod)

	def new_mod(self, new):
		self.mod = new
		return

	def my_config(self):
		return self.fixstr(self.config) + self.my_id()

	def new_config(self, new):
		self.config = new
		return

	def my_data(self):
		return self.fixstr(self.data) + self.my_id() + "/" + self.new_fn()

	def new_data(self, new):
		self.data = new
		return

	def my_usr(self):
		return self.fixstr(self.usr)

	def new_usr(self, new):
		self.usr = new
		return

	def my_token(self):
		return base64.b64decode(self.token)

	def new_token(self, new):
		self.token = new
		return

	def my_repo(self):
		return self.fixstr(self.repo)

	def new_repo(self, new):
		self.repo = new
		return

	def my_pk(self):
		return self.pk

	def new_pk(self, new):
		self.pk = new
		self.pk = self.import_key()
		return

	def import_key(self):
		self.pk = RSA.importKey(self.pk)
		self.PKCS1_OAEP.new(self.pk)
		return

	def my_size(self):
		return self.size

	def new_size(self, new):
		self.size = new
		return

	def my_pwd(self):
		return self.fixstr(self.pwd)

	def new_pwd(self, new):
		self.pwd = new
		return

	def my_sleep(self):
		return self.sleep

	def new_sleep(self, new):
		self.sleep = new
		return

	def new_fn(self):
		i_time = int(time.time())
		fn = str(i_time) + self.fixstr(self.fn_s)
		return xxhash.xxh64(fn).hexdigest()

	def com_mess(self):
		com = str(time.time())
		return xxhash.xxh64(com).hexdigest()

	def fixstr(self, t_str):
		n_str = ""
		for c in t_str:
			if re.match("[a-zA-Z_./]", c) != None:
				n_str += c
		return n_str
