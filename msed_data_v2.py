import struct,random

trunc_level=8

f=open("movable.sed","rb")
buf=f.read()
f.close()
o=0x110
lfcs=struct.unpack("<I",buf[o+0:o+4])[0]
msed1=struct.unpack("<I",buf[o+4:o+8])[0]
msed3=struct.unpack("<I",buf[o+12:o+16])[0]&0x7FFFFFFF
print(hex(lfcs),hex(msed1),hex(msed3))

est=lfcs//5-msed3
isnew=2
if(msed1):
	isnew=3
print(hex(est))
print(est)
lfcs>>=trunc_level
lfcs<<=trunc_level 
lfcs|= (1<<(trunc_level-1))
f=open("msed_data_v2_%08X.bin" % random.randint(0,0xFFFFFFFF),"wb")
f.write(struct.pack("<I",lfcs))
f.write(struct.pack("<i",est))
f.write(struct.pack("<I",isnew))
f.close()