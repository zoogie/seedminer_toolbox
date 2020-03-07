#put your lfcs inside below quotes
LFCS="0204ff5678" 

#put your id0 inside below quotes
ID0="0123456789abcdef0123456789abcdef"	

#note: both numbers need to be hex, but don't preface them with the 0x


import struct,sys
pad=b"\x00"

lfcs_int=int(LFCS,16)
isnew=lfcs_int>>32
lfcs_base=lfcs_int & 0xffffffff

if LFCS=="0204ff5678":
	print("Error: you seem to have left the example LFCS unchanged, it needs to be YOUR LFCS!")
	sys.exit(6)
if ID0=="0123456789abcdef0123456789abcdef":
	print("Error: you seem to have left the example ID0 unchanged, it needs to be YOUR ID0!")
	sys.exit(7)

if len(ID0) != 32:
	print("Error: ID0 needs to be exactly 32 hex characters")
	print("Actual number of digits: %d" % len(ID0))
	sys.exit(1)

if isnew == 0: 
	if lfcs_base > 0x0B000000:
		print("Error: LFCS is far too large to be possible, recheck your input")
		sys.exit(2)
elif isnew == 2:
	if lfcs_base > 0x05000000:
		print("Error: LFCS is far too large to be possible, recheck your input")
		sys.exit(3)
else:
	print("Error: incorrect LFCS format, 5th byte isn't 0 or 2, or non-zero digits on 6th byte or above")
	sys.exit(4)
	
if lfcs_base < 0x50000:
	print("Error: LFCS is far too small to be possible, recheck your input")
	sys.exit(5)	
	
with open("movable_part1.sed","wb") as f:
	part1=struct.pack("<Q", lfcs_int)
	part1+=pad*8
	try:
		part1+=bytes(ID0,"ascii")
	except:
		part1+=bytes(ID0)
	part1+=pad*(0x1000-0x30)
	if len(part1) != 0x1000:
		print("Error: output file is not expected size")
		sys.exit(8)
	f.write(part1)

print("movable_part1.sed generated successfully")