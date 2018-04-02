import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
import codecs,urllib2,struct,os,sys

'''
first run these commands to get the .xml databases needed for this script, then choose the region below this comment.
wget --output-document=title_us.xml --no-check-certificate "https://samurai.ctr.shop.nintendo.net/samurai/ws/US/titles?shop_id=1&limit=3000&offset=0"
wget --output-document=title_eu.xml --no-check-certificate "https://samurai.ctr.shop.nintendo.net/samurai/ws/GB/titles?shop_id=1&limit=3000&offset=0"
wget --output-document=title_jp.xml --no-check-certificate "https://samurai.ctr.shop.nintendo.net/samurai/ws/JP/titles?shop_id=1&limit=3000&offset=0"
'''

region="eu"
# us eu jp

def download(url, dest):
	try:
		response = urllib2.urlopen(url)
		html = response.read()
		length=len(html)
		if(length):
			f=open(dest,"wb")
			f.write(html)
			f.close()
			#print("Download "+dest+" success!")
			return html
		else:
			print("Wrong size "+hex(length)+" "+dest)

	except:
		print("Error updating "+dest)

tidh="\x00\x04\x80\x04"
tree = ET.parse("title_"+region+".xml")
root = tree.getroot()

elem = root.iter("title")
sv=0x19a
ss=0xb0c
sdu=0x34c000
sde=0x366000
sv=0x19a
ss=0xb0c
save_size=0
srl_size=0
b=0
c=0
e=0
m=0
if(region=="us"):
	sud=sdu
elif(region=="eu"):
	sud=sde
else:
	print("Region error")
	sys.exit(0)
out=u""
iout=u""

for title in elem:
	pcode = title.find('product_code').text
	if "TWL-N" in pcode:
		tid=(tidh+pcode[6:10]).encode('hex')
		tidlow=(pcode[6:10]+".bin").encode('hex')
		#print(tid)
		temp=download("http://nus.cdn.c.shop.nintendowifi.net/ccs/download/%s/tmd" % tid,"tmd_all/"+region+"_"+tid+"_"+pcode[6:10]+".tmd")
		#http://nus.cdn.c.shop.nintendowifi.net/ccs/download/000480045a324154/tmd 000480044b51394a
		save_size=struct.unpack("<I",temp[sv:sv+4])[0]
		srl_size=struct.unpack(">Q",temp[ss:ss+8])[0]
		#print(hex(save_size))
		eshop_url="ESHOP://"+title.find('id')
		info="%s - %s\nsave_size=0x%08X srl_size=0x%08X" % (pcode[6:10],tidlow,save_size,srl_size)
		if(save_size>=(0x4000) and srl_size>=sud):
			out+=title.find('name').text+"\n"+info+"\nCompatible: YES!\n----------------------------------------\n"
			print("compat %s" % (tid))
			b+=1
		else:
			out+=title.find('name').text+"\n"+info+"\nCompatible: NO\n----------------------------------------\n"
			print("incompat %s" % (tid))
			m+=1
			
		c+=1


print(b,c)
print(m,c)
print((b+0.0)/(c+0.0))
print(e)
f=codecs.open("compat_%s.txt" % region,"w",encoding='utf-8')
f.write(out)
f.close()