import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import struct

dotsize=1.5
linesize=0.25

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

old=lfcs_len-1
new=lfcs_new_len-1
tot=old+new
title="old3ds:%s + new3ds:%s = %s" %(str(old),str(new),str(tot))

for i in range(lfcs_new_len):
	lfcs_new.append(struct.unpack("<i",buf[i*8:i*8+4])[0]<<12 or 0x800)

for i in range(lfcs_new_len):
	ftune_new.append(struct.unpack("<i",buf[i*8+4:i*8+8])[0])
	
def graph():
	plt.figure(figsize=(14,5))
	plt.suptitle(title)
	axes = plt.gca()
	axes.get_xaxis().set_major_formatter(ticker.FormatStrFormatter("%X"))
	plt.plot(lfcs,ftune,'--bo',markersize=dotsize,linewidth=linesize)
	plt.plot(lfcs_new,ftune_new,'--ro',markersize=dotsize,linewidth=linesize)
	plt.axhline(0, color='gray')
	plt.axvline(0, color='gray')
	plt.xlabel('LFCS (blue=old3ds, red=new3ds)')
	plt.ylabel('msed3 error')

graph()
plt.show()
graph() #bug workaround - savefig will remove the toolbar from view if used before show()
plt.savefig("msed_data_%08d.png" % tot)