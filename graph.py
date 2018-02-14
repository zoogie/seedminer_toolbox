import matplotlib.pyplot as plt
import struct
'''
X = range(10)
plt.plot(X, [x*x for x in X])
plt.show()
'''

f=open("lfcs.dat","rb")
buf=f.read()
f.close()

lfcs_len=len(buf)/8
lfcs=[]
ftune=[]
err_correct=0


for i in range(lfcs_len):
	lfcs.append(struct.unpack("<i",buf[i*8:i*8+4])[0]<<12 or 0x800)

for i in range(lfcs_len):
	ftune.append(struct.unpack("<i",buf[i*8+4:i*8+8])[0])

f=open("lfcs_new.dat","rb")
buf=f.read()
f.close()

lfcs_new_len=len(buf)/8
lfcs_new=[]
ftune_new=[]

print("OLD3DS="+str(lfcs_len-1))
print("NEW3DS="+str(lfcs_new_len-1))
print("TOTAL="+str(lfcs_new_len+lfcs_len-2))

for i in range(lfcs_new_len):
	lfcs_new.append(struct.unpack("<i",buf[i*8:i*8+4])[0]<<12 or 0x800)

for i in range(lfcs_new_len):
	ftune_new.append(struct.unpack("<i",buf[i*8+4:i*8+8])[0])
plt.figure(figsize=(12,4))
plt.plot(lfcs,ftune,'--bo')
plt.plot(lfcs_new,ftune_new,'--ro')
plt.axhline(0, color='gray')
plt.axvline(0, color='gray')

plt.show()