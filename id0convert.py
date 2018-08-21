import os,sys,hashlib

with open(sys.argv[1],"rb") as f:
	msed=f.read(0x120)
	keyy=msed[0x110:0x120]
	sha256=hashlib.sha256(keyy).digest()[:0x10]

id0=sha256[3::-1] + sha256[7:3:-1] + sha256[11:7:-1] + sha256[15:11:-1]

print(id0.encode("hex"))