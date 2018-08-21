import struct,random

f=open("movable.sed","rb")
buf=f.read()
f.close()
o=0x110
lfcs=struct.unpack("<I",buf[o+0:o+4])[0]
msed1=struct.unpack("<I",buf[o+4:o+8])[0]
msed3=struct.unpack("<I",buf[o+12:o+16])[0]&0x7FFFFFFF
print(hex(lfcs),hex(msed1),hex(msed3))

est=lfcs//5-msed3
isnew=0
if(msed1):
	isnew=1
print(hex(est))
print(est)
lfcs>>=12
f=open("msed_data_%08X.bin" % random.randint(0,0xFFFFFFFF),"wb")
f.write(struct.pack("<I",lfcs))
f.write(struct.pack("<i",est))
f.write(struct.pack("<I",isnew))
f.close()