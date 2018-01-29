import os,sys,struct,glob

def byteSwap4(n):
	return n[3]+n[2]+n[1]+n[0]

def backup(fn,buf):
	g=open(fn,"wb")
	g.write(buf)
	g.close()

	
###############################################################  dupe check
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

for i in input0:
	f=open(i,"rb")
	bufin=f.read()
	f.close()
	if(bufin[8:]=="\x00\x00\x00\x00"):
		for a in range(lfcs_len):
			temp=buf0[a*8:a*8+4]
			if(temp in bufin[:8]):
				print(str(i)+" is already in old3ds database!!")
				print(str(a)+" record number\n")
				match+=1
			
	elif(bufin[8:]=="\x01\x00\x00\x00"):
		for b in range(lfcs_new_len):
			temp=buf1[b*8:b*8+4]
			if(temp in bufin[:8]):
				print(str(i)+" is already in new3ds database!!")
				print(str(b)+" record number\n")
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
	elif(buf[8:]=="\x00\x00\x00\x00"):
		temp=byteSwap4(buf[0:4])+buf[4:8]
		lfcs.append(struct.unpack(">Q",temp)[0])
		lfcs_len+=1
	else:
		print("Error: input file could not be parsed")
		
'''
for i in range(lfcs_len):
	lfcs[i]=byteSwap4(lfcs[[0:4])+i[4:8]
for i in lfcs_new:
	i=byteSwap4(i[0:4])+i[4:8]
'''
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


			