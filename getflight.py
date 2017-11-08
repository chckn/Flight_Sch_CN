import urllib2
from lxml import etree
import re
def request():
	response=urllib2.urlopen("http://jipiao.oklx.com/cn_airfield_schedule.aspx")
	html=response.read().decode('gb2312')
	b=re.compile(r"href=\"\/cnschedule\/(\w+_\d.html)\"",re.MULTILINE)
	lst=b.findall(html)
	return lst
