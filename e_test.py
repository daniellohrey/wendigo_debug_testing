import rsa
import base64

msg = b"please work"

pub, priv = rsa.newkeys(2048)
#print public
#print private

#enc = base64.b64encode(rsa.encrypt(msg, pub))
#print enc
#dec = rsa.decrypt(base64.b64decode(enc), priv)
#print dec

enc = base64.b64encode(rsa.encrypt(msg, priv))
print enc
dec = rsa.decrypt(base64.b64decode(enc), priv)
print dec
