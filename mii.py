from Cryptodome.Cipher import AES

nk31=0x59FC817E6446EA6190347B20E9BDCE52
f=open("input.bin","rb")
enc=f.read()
f.close()

def int16bytes(n):
	s=""
	for i in range(16):
		s=chr(n & 0xFF)+s
		n=n>>8
	return s

def decrypt(message, key, nonce):
	cipher = AES.new(key, AES.MODE_CCM, nonce )
	return cipher.decrypt(message)

nonce=enc[:8]+"\x00"*4
dec=decrypt(enc[8:0x60],int16bytes(nk31),nonce)
nonce=nonce[:8]
final=dec[:12]+nonce+dec[12:]

f=open("output.bin","wb")
f.write(final)
f.close()