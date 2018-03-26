import os,sys,urllib2,glob,struct

q=[2106,2075,2070,2033,2024,2011,2009]

begin=q[1]
end=q[0]
print(begin,end)

def download(url, dest):
	try:
		response = urllib2.urlopen(url)
		html = response.read()
		length=len(html)
		if(length==0xC):
			f=open(dest,"wb")
			f.write(html)
			f.close()
			print("Download "+dest+" success!")
		else:
			print("Wrong size "+hex(length)+" "+dest)
	except:
		print("Error updating "+dest)

for i in range(begin+1,end+1):    #https://git.nelthorya.net/blackfire/msed_data/
	url="https://git.nelthorya.net/blackfire/msed_data/raw/master/msed_data_"+str(i)+".bin?raw=true"
	dest="seed/msed_2/movable_"+str(i)+".sed"
	download(url, dest)
count=0
mdata=[]
dir=glob.glob("seed/msed_2/*")
for i in dir:
	f=open(i,"rb")
	mdata.append(f.read())
	f.close()
mdata=set(mdata)
for i in mdata:
	f=open("seed/msed_3/msed_data_%d.bin" % count,"wb")
	f.write(i)
	f.close()
	count+=1