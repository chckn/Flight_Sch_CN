#-*- coding: utf-8 -*-
import urllib3
import csv
from lxml import etree
import re
def request():
	http=urllib3.PoolManager()
	
	response=http.request("GET","http://jipiao.oklx.com/cn_airfield_schedule.aspx")
	html=response.data.decode('gb2312')
	b=re.compile(r"href=\"\/(cnschedule\/\w+_\d.html)\"",re.MULTILINE)
	lst=b.findall(html)
	return lst

def onepage(page):
	url="http://jipiao.oklx.com/"+page
	http=urllib3.PoolManager()

	response=http.request("GET",url)
	html=response.data.decode('gb2312')
	tree=etree.HTML(html)
	r=tree.xpath("//table[@class='xpTable']/tr")

	return r


def main():
	with open("result.csv","w", encoding='utf-8') as csvfile:
		fieldname=[u'Flight',u'Carrier',u'Origin',u'Dest',u'Dep',u'Arr',u'Freq',u'Model']

		writer=csv.DictWriter(csvfile, fieldname)
		writer.writeheader()
		
		pages=request()
		for p in pages:
			lines=onepage(p)
			for ldx in range(1,len(lines)):
				l=oneline(lines[ldx].findall("td"))
				writer.writerow(l)
			
def oneline(b):
	data={}
	data[u"Flight"]=b[0].find("img").tail.strip()
	data[u"Carrier"]=b[1].text.strip()
	data[u"Origin"]=b[2].find("a").text.strip()
	data[u"Dep"]=b[3].text.strip()
	data[u"Dest"]=b[4].find("a").text.strip()
	data[u"Arr"]=b[5].text.strip()
	data[u"Freq"]=b[6].text.strip()
	data[u"Model"]=b[7].text.strip()
	return data

main()
