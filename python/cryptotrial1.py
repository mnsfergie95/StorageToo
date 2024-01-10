from Crypto.Hash import SHA256
hash = SHA256.new()
hash.update('message'.encode("utf8"))
print(hash.digest())
#'\xabS\n\x13\xe4Y\x14\x98+y\xf9\xb7\xe3\xfb\xa9\x94\xcf\xd1\xf3\xfb"\xf7\x1c\xea\x1a\xfb\xf0+F\x0cm\x1d'

from Crypto.Cipher import AES
obj = AES.new('This is a key123'.encode("utf8"), AES.MODE_CBC, 'This is an IV456'.encode("utf8"))
message = "The answer is no"
ciphertext = obj.encrypt(message.encode("utf8"))
print(ciphertext)
obj2 = AES.new('This is a key123'.encode("utf8"), AES.MODE_CBC, 'This is an IV456'.encode("utf8"))
print(obj2.decrypt(ciphertext))