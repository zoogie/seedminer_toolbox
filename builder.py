import os,sys,struct,glob,binascii

def byteSwap4(n):
	return n[3]+n[2]+n[1]+n[0]

def backup(fn,buf):
	g=open(fn,"wb")
	g.write(buf)
	g.close()

	
###############################################################  dupe checks
f=open("lfcs.dat","rb")
buf0=f.read()
f.close()
lfcs_len=len(buf0)/8

f=open("lfcs_new.dat","rb")
buf1=f.read()
f.close()
lfcs_new_len=len(buf1)/8


match=0
input0=glob.glob("new/*")

self_buf=[]
fname_buf=[]
error=0
for i in input0:
	f=open(i,"rb")
	temp=f.read()
	if(len(temp) != 12):
		print("Wrong size file in input! %s" % i)
		error=1
	temp=temp[:4]+temp[8:] 
	self_buf.append(temp)
	fname_buf.append(i)
	f.close()
if(error):
	print("Aborting...")
	sys.exit(0)

sanity_level=100
dupe=0
while(len(self_buf) != len(set(self_buf))):
	print("Duplicates found in input!")
	for i in range(len(self_buf)):
		count=self_buf.count(self_buf[i])
		if(count > 1):
			print("%s %08X   %s" % (str(count), binascii.crc32(self_buf[i]) & 0xffffffff, fname_buf[i]))
			os.remove(fname_buf[i])
			del fname_buf[i]
			del self_buf[i]
			del input0[i]
			print("removed")
			dupe=1
			break

	sanity_level-=1
	if(sanity_level<0):
		print("Too many duplicates in input to contend with!")
		sys.exit(0)
	
if(dupe): 
	print("Input should now be clean of dupes, please re-run")
	sys.exit(0)

for j in range(2):
	match=0
	for i in input0:
		try:
			f=open(i,"rb")
			bufin=f.read()
			f.close()
		except:
			print("%s not found" % i)
			continue
	
		if(bufin[8:]=="\x00\x00\x00\x00"):
			for a in range(lfcs_len):
				temp=buf0[a*8:a*8+4]
				if(temp in bufin[:4]):
					print("%-30s already in old3ds database!! %s/%s" % (str(i),str(a),str(lfcs_len)))
					os.system("rm %s" % i)
					print("removing...")
					match+=1
				
		elif(bufin[8:]=="\x01\x00\x00\x00"):
			for b in range(lfcs_new_len):
				temp=buf1[b*8:b*8+4]
				if(temp in bufin[:4]):
					print("%-30s already in new3ds database!! %s/%s" % (str(i),str(b),str(lfcs_new_len)))
					os.system("rm %s" % i)
					print("removing...")
					match+=1
		else:
			print("Error: input file could not be parsed")

		

print(str(match)+" matches")
if(match>0):
	print("Matches found, terminating...\n")
	exit()

#############################################################

f=open("lfcs.dat","rb")
buf=f.read()
f.close()
backup("lfcs.dat.backup",buf)

lfcs_len=len(buf)/8
lfcs=[]

for i in range(lfcs_len):
	temp=byteSwap4(buf[i*8:i*8+4])+buf[i*8+4:i*8+8]
	lfcs.append(struct.unpack(">Q",temp)[0])

f=open("lfcs_new.dat","rb")
buf=f.read()
f.close()
backup("lfcs_new.dat.backup",buf)

lfcs_new_len=len(buf)/8
lfcs_new=[]

for i in range(lfcs_new_len):
	temp=byteSwap4(buf[i*8:i*8+4])+buf[i*8+4:i*8+8]
	lfcs_new.append(struct.unpack(">Q",temp)[0])
	
input=glob.glob("new/*")

for i in input:
	f=open(i,"rb")
	buf=f.read()
	f.close()
	if(buf[8:]=="\x01\x00\x00\x00"):
		temp=byteSwap4(buf[0:4])+buf[4:8]
		lfcs_new.append(struct.unpack(">Q",temp)[0])
		lfcs_new_len+=1
		print("%-30s added to new3ds database" % i)
	elif(buf[8:]=="\x00\x00\x00\x00"):
		temp=byteSwap4(buf[0:4])+buf[4:8]
		lfcs.append(struct.unpack(">Q",temp)[0])
		lfcs_len+=1
		print("%-30s added to old3ds database" % i)
	else:
		print("Error: input file could not be parsed")
		
lfcs.sort()
lfcs_new.sort()

f=open("lfcs.dat","wb")
for i in range(lfcs_len):
	temp=struct.pack(">Q",lfcs[i])
	temp=byteSwap4(temp[0:4])+temp[4:8]
	f.write(temp)
f.close()

f=open("lfcs_new.dat","wb")
for i in range(lfcs_new_len):
	temp=struct.pack(">Q",lfcs_new[i])
	temp=byteSwap4(temp[0:4])+temp[4:8]
	f.write(temp)
f.close()
#exit()


			