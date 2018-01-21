from __future__ import print_function
import os,sys,glob

buf=""
hashcount=0

f=open("movable_part1.sed","rb")
file=f.read()
f.close()
f=open("movable_part1.sed.backup","wb")
f.write(file)
f.close()

trim=0
try:
	trim=file.index("\x00"*0x40)
	file=file[:trim]
except:
	pass
	

dirs=glob.glob("*")

for i in dirs:
	try:
		print(i,end='')
		int(i,16)
		if(len(i)==32 and i not in file):
			buf+=i
			hashcount+=1
		else:
			print(" -- improper ID0 length or already in file",end='')
		print("")
	except:
		print(" -- not an ID0")
	
print("")
if(hashcount>1):
	print("Too many ID0 dirs! (%d)\nMove the ones your 3ds isn't using!" % (hashcount))
	exit()

if(hashcount==1):
	print("Hash added!")
else:
	print("No hashes added!")
pad_len=0x1000-len(file+buf)
pad="\x00"*pad_len
f=open("movable_part1.sed","wb")
f.write(file+buf+pad)
f.close()
print("There are now %d ID0 hashes in your movable_part1.sed!" % ((len(file+buf)/0x20)))
print("Done!")