import requests, re, os
from time import sleep
from html import unescape as hd


from bs4 import BeautifulSoup as html
from bs4 import BeautifulSoup
def cleanhtml(raw_html):
	cleanr = re.compile('<.*?>')
	cleantext = re.sub(cleanr, "", raw_html)
	return cleantext

def delayTimer (time):
	for i in range (time, 0, -1):
		print ("Hãy chờ %d giây  " % i, end = "\r")
		sleep (1)
def getStoryWattpad (url):
	headers = {
		"user-agent": "Mozilla/5.0 (Linux; Android 11; RMX3195) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Mobile Safari/537.36"
	}
	print ("ĐANG GET TRUYỆN TẠI WATTPAD.COM")
	res = requests.get (url, headers = headers).text
	folderName = res.split ('<title>')[1].split ('</title>')[0]
	folderName = folderName.replace (":"," - ")
	folderName = folderName.replace ('.', '-').replace ("?","").replace ('(', '').replace (')','').replace ('[','').replace ('|','').replace (']','').replace ('_','').replace ('-','')
	folderName = folderName.replace ("\r", "").replace ("\n", "").replace ('\\r', "").replace ('\\n', '')
	print ("Đang Get Bộ %s" % folderName)
	if not os.path.exists (folderName):
		os.makedirs (folderName)
	files = open (folderName + "/Tonghop.html", "a+", encoding="utf-8")
	files.write ("<h1>" + folderName + "</h1><br/>")
	data = html (res, "html.parser")
	listChap = str (data.find ('div', class_="story-parts"))
	data = html (listChap, 'html.parser')
	data = (data.find_all ('li'))
	listInfo = []
	PATH = "https://wattpad.com"
	for i in data:
		nameChap = (i.find ('div', class_="part__label").text)
		href = PATH + (i.find ('a').get('href'))
		jsons = {"name":nameChap,"href":href}
		listInfo.append (jsons)
	for j in listInfo:
		urls = j["href"]
		fileName = j['name'].lower ()
		while True:
			if fileName[0] == " ":
				fileName = fileName[1:]
			else:
				break
		fileName = fileName.replace (":"," - ")
		fileName = fileName.replace ('.', '-').replace ("?","").replace ('(', '').replace (')','').replace ('[','').replace ('|','').replace (']','').replace ('_','').replace ('-','')
		fileName = fileName.replace ("\r", "").replace ("\n", "").replace ('\\r', "").replace ('\\n', '')
		res = requests.get (urls, headers = headers).text
		pages = int (res.split ('"pages":')[1].split (',')[0]) + 1
		textContent = ""
		for i in range (1, int (pages), +1):
			url = urls + "/page/%d" % i
			res = requests.get (url, headers = headers).text
			data = (hd (res).split ('"storyText":"')[1].split ('","page"')[0])
			data = data.replace ("</p>", "\n")
			data = cleanhtml (data)
			data = data.replace ("\n", "</br>")
			textContent += data
			textContent = textContent.replace ('\\n', "")
			file = open (folderName + "/" + fileName.replace (':', '-') + ".html", "w+", encoding="utf-8")
			file.write ("<h1>" + fileName + "</h1><br/>")
			file.write (textContent)
			file.close ()
			files.write (textContent)
		print ("Get xong chương: %s" % fileName)
	files.close ()
	print ("Đã get xong bộ %s" % folderName)

def getStoryWikidth (url):
	print ("ĐANG LẤY TRUYỆN TẠI WIKIDTH.COM")
	headers = {
		"user-agent":"Mozilla/5.0 (Linux; Android 11; RMX3195) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36"
	}
	path = "https://wikidth.com"
	response = requests.get (url, headers = headers).text
	if "banned your IP address" in response:
		print ('Vui lòng đổi ip và thử lại')
		return
	folderName = response.split ('<title>')[1].split ('</title>')[0]
	if not os.path.exists (folderName):
		os.makedirs (folderName)
	else:
		pass
	files = open (folderName + "/Tonghop.html", "a+", encoding="utf-8")
	files.write ("<h1>" + folderName + "<h1/><br/>")
	print ("Đang get bộ %s" % folderName)
	chapUrl = response.split ('<a class="btn waves-effect waves-light orange-btn" href="')[1].split ('"')[0]
	url = path + chapUrl
	chapNum = 0
	while True:
		res = requests.get (url, headers = headers).text
		if "banned your IP address" in res:
			print ('Vui lòng đổi ip và thử lại')
			break
		try:
			chapNum = chapNum + 1
			content = (res.split ('<div id="bookContentBody" class="" data-activates='+"'ddAddName'"+' style="margin-top: 1rem">')[1].split ('</div>')[0])
			content = content.replace ('</p>', "\n")
			content = cleanhtml (content)
			content = "<h1>Chap " + str (chapNum) + "</h1><br/>" + content.replace ("\n", "<br/><br/>")
			file = open (folderName + "/Chapter" + str (chapNum) + ".html", "w+", encoding="utf-8")
			file.write (content)
			file.close ()
			files.write (content+"<br/>")
			nextChap = res.split ('<a id="btnNextChapter" href="')[1].split ('"')[0]
			url = path + nextChap
			print ("Đã get xong chap: %d" % chapNum)
		except Exception:
			break
		sleep (3)
	print ("Đã get xong bộ %s" % folderName)




def getStoryTruyenfull (url):
	headers = {
		"user-agent":"Mozilla/5.0 (Linux; Android 11; RMX3195) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36"
	}
	res = requests.get (url, headers = headers).text
	folderName = res.split ('<title>')[1].split ('</title>')[0]
	print ("ĐANG GET TRUYỆN TẠI TRUYENFULL.COM")
	print ("Đang get bộ %s" % folderName)
	if not os.path.exists (folderName):
		os.makedirs (folderName)
	files = open (folderName + '/Tonghop.html', 'a+', encoding="utf-8")
	files.write ("<h1>" + folderName + "</h1><br/>")
	for i in range (1, 99999, +1):
		urls = url + "chuong-" + str(i) + "/"
		result = requests.get (urls, headers = headers).text
		try:
			title = result.split ('<title>')[1].split ('</title>')[0]
			chap = "<h1>" + title + "</h1><br/>"
			content = result.split ('<div id="chapter-c" class="chapter-c"><div class="visible-md visible-lg ads-responsive incontent-ad" id="ads-chapter-pc-top" align="center" style="height:90px"></div>')[1].split ('</div>')[0].replace ('</p>', "\n")
			content = chap + cleanhtml (content).replace ("\n", "<br/>")
			file = open (folderName + "/Chapter" + str (i) + ".html", "w+", encoding="utf-8")
			file.write (content)
			file.close ()
			files.write (content)
			print ("Get xong chương: %d" % i)
		except Exception:
			print ("Đã get xong bộ %s" % folderName)
			files.close ()
			break
def getStoryTruyentr (url):
	headers = {
		"user-agent":"Mozilla/5.0 (Linux; Android 11; RMX3195) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36"
	}
	res = requests.get (url, headers = headers).text
	folderName = res.split ('<h1 class="title">')[1].split ('</h1>')[0]
	folderName = cleanhtml (folderName).replace ("\n", "")
	print ("ĐANG GET TRUYỆN TẠI TRUYENTR.INFO")
	print ("Đang get bộ %s" % folderName)
	if not os.path.exists (folderName):
		os.makedirs (folderName)
	files = open (folderName + '/Tonghop.html', "a+", encoding="utf-8")
	files.write ("<h1>" + folderName + "</h1></br>")
	for i in range (1, 99999, +1):
		try:
			urls = url + "chuong-%d/" % i
			res = requests.get (urls, headers = headers).text
			title = "<h1>" + res.split ('<title>')[1].split ('</title>')[0] + "</h1><br/>"
			content = (res.split ('<div class="content container1 chapter-c">')[1].split ('<div class="pagination chapter-nav chapter-nav-bottom">')[0])
			content = content.replace ('<br />', "\n")
			content = title + cleanhtml (content).replace ("\n", "<br/>").replace ('(adsbygoogle = window.adsbygoogle || []).push({});', "")
			file = open (folderName + "/Chapter" + str (i) + ".html", "w+", encoding="utf-8")
			file.write (content)
			file.close ()
			files.write (content)
			print ("Đã get chương: %d" % i)
		except Exception:
			print ("Đã get xong bộ %s" % folderName)
			break
			files.close ()

def getStoryWikinuNet (url):
	print ("Bạn Đang GET Truyện Tại WIKINU.NET")
	host = 'https://wikinu.net'
	h = {
		"user-agent": "Mozilla/5.0 (Linux; Android 11; RMX3195) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.92 Mobile Safari/537.36"
	}
	result = requests.get (url, headers = h).text
	Soup = BeautifulSoup (result, "html.parser")
	title = Soup.title.text
	folderName = title.replace (":"," - ")
	folderName = folderName.replace ('.', '-').replace ("?","").replace ('(', '').replace (')','').replace ('[','').replace ('|','').replace (']','').replace ('_','').replace ('-','')
	folderName = folderName.replace ("\r", "").replace ("\n", "").replace ('\\r', "").replace ('\\n', '')
	print ("Đang get bộ %s" % folderName)
	if not os.path.exists (folderName):
		os.makedirs (folderName)
	files = open (folderName + "/Tonghop.html", "a+", encoding="utf-8")
	files.write ("<h1>" + folderName + "</h1><br/>")
	startChap = Soup.find_all ("div", class_ = "control-btns")
	startChap = startChap[0].find_all ('a')
	url = host + startChap[0]["href"]
	chapTotal = 0
	while True:
		chapTotal = chapTotal + 1
		data = requests.get (url, headers = h).text
		Soup = BeautifulSoup (data, "html.parser")
		title = Soup.find_all ('div', id = "bookContent")
		title = title[0].find_all ('p')[1].text
		fileName = title.replace (":"," - ")
		fileName = fileName.replace ('.', '-').replace ("?","").replace ('(', '').replace (')','').replace ('[','').replace ('|','').replace (']','').replace ('_','').replace ('-','')
		fileName = fileName.replace ("\r", "").replace ("\n", "").replace ('\\r', "").replace ('\\n', '')
		file = open (folderName + "/" + fileName + ".html", "w+", encoding = "utf8")
		file.write ("<h1>" + fileName + "</h1><br/>")
		files.write ("<h1>" + fileName + "</h1><br/>")
		content = Soup.find_all ('div', id = 'bookContentBody')
		content = str (content[0])
		file.write (content)
		files.write (content)
		file.close ()
		print ("Đã get xong chap %d" % chapTotal)
		nextChap = Soup.find_all ('a', class_ = "btn-bot")
		for i in nextChap:
			if "chương sau" in i.text.lower ():
				nextChap = host + i["href"]
				break
			else:
				nextChap = None
		if nextChap is None:
			print ("Hoàn Thành Bộ %s" % folderName)
			files.close ()
			break
		else:
			url = nextChap
		delayTimer (10)

def getStoryWikidthNet (url):
	print ("Bạn Đang GET Truyện Tại WIKIDTH.NET")
	host = 'https://wikidth.net'
	h = {
		"user-agent": "Mozilla/5.0 (Linux; Android 11; RMX3195) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.92 Mobile Safari/537.36"
	}
	result = requests.get (url, headers = h).text
	Soup = BeautifulSoup (result, "html.parser")
	title = Soup.title.text
	folderName = title.replace (":"," - ")
	folderName = folderName.replace ('.', '-').replace ("?","").replace ('(', '').replace (')','').replace ('[','').replace ('|','').replace (']','').replace ('_','').replace ('-','')
	folderName = folderName.replace ("\r", "").replace ("\n", "").replace ('\\r', "").replace ('\\n', '')
	print ("Đang get bộ %s" % folderName)
	if not os.path.exists (folderName):
		os.makedirs (folderName)
	files = open (folderName + "/Tonghop.html", "a+", encoding="utf-8")
	files.write ("<h1>" + folderName + "</h1><br/>")
	startChap = Soup.find_all ("div", class_ = "control-btns")
	startChap = startChap[0].find_all ('a')
	url = host + startChap[0]["href"]
	chapTotal = 0
	while True:
		chapTotal = chapTotal + 1
		data = requests.get (url, headers = h).text
		Soup = BeautifulSoup (data, "html.parser")
		title = Soup.find_all ('div', id = "bookContent")
		title = title[0].find_all ('p')[1].text
		fileName = title.replace (":"," - ")
		fileName = fileName.replace ('.', '-').replace ("?","").replace ('(', '').replace (')','').replace ('[','').replace ('|','').replace (']','').replace ('_','').replace ('-','')
		fileName = fileName.replace ("\r", "").replace ("\n", "").replace ('\\r', "").replace ('\\n', '')
		file = open (folderName + "/" + fileName + ".html", "w+", encoding = "utf8")
		file.write ("<h1>" + fileName + "</h1><br/>")
		files.write ("<h1>" + fileName + "</h1><br/>")
		content = Soup.find_all ('div', id = 'bookContentBody')
		content = str (content[0])
		file.write (content)
		files.write (content)
		file.close ()
		print ("Đã get xong chap %d" % chapTotal)
		nextChap = Soup.find_all ('a', class_ = "btn-bot")
		for i in nextChap:
			if "chương sau" in i.text.lower ():
				nextChap = host + i["href"]
				break
			else:
				nextChap = None
		if nextChap is None:
			print ("Hoàn Thành Bộ %s" % folderName)
			files.close ()
			break
		else:
			url = nextChap
		delayTimer (10)


def getStoryWikiSach (url):
	print ("Bạn Đang GET Truyện Tại WIKISACH.COM")
	host = 'https://wikisach.com'
	h = {
		"user-agent": "Mozilla/5.0 (Linux; Android 11; RMX3195) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.92 Mobile Safari/537.36"
	}
	result = requests.get (url, headers = h).text
	Soup = BeautifulSoup (result, "html.parser")
	title = Soup.title.text
	folderName = title.replace (":"," - ")
	folderName = folderName.replace ('.', '-').replace ("?","").replace ('(', '').replace (')','').replace ('[','').replace ('|','').replace (']','').replace ('_','').replace ('-','')
	folderName = folderName.replace ("\r", "").replace ("\n", "").replace ('\\r', "").replace ('\\n', '')
	print ("Đang get bộ %s" % folderName)
	if not os.path.exists (folderName):
		os.makedirs (folderName)
	files = open (folderName + "/Tonghop.html", "a+", encoding="utf-8")
	files.write ("<h1>" + folderName + "</h1><br/>")
	startChap = Soup.find_all ("div", class_ = "control-btns")
	startChap = startChap[0].find_all ('a')
	url = host + startChap[0]["href"]
	chapTotal = 0
	while True:
		chapTotal = chapTotal + 1
		data = requests.get (url, headers = h).text
		Soup = BeautifulSoup (data, "html.parser")
		title = Soup.find_all ('div', id = "bookContent")
		title = title[0].find_all ('p')[1].text
		fileName = title.replace (":"," - ")
		fileName = fileName.replace ('.', '-').replace ("?","").replace ('(', '').replace (')','').replace ('[','').replace ('|','').replace (']','').replace ('_','').replace ('-','')
		fileName = fileName.replace ("\r", "").replace ("\n", "").replace ('\\r', "").replace ('\\n', '')
		file = open (folderName + "/" + fileName + ".html", "w+", encoding = "utf8")
		file.write ("<h1>" + fileName + "</h1><br/>")
		files.write ("<h1>" + fileName + "</h1><br/>")
		content = Soup.find_all ('div', id = 'bookContentBody')
		content = str (content[0])
		file.write (content)
		files.write (content)
		file.close ()
		print ("Đã get xong chap %d" % chapTotal)
		nextChap = Soup.find_all ('a', class_ = "btn-bot")
		for i in nextChap:
			if "chương sau" in i.text.lower ():
				nextChap = host + i["href"]
				break
			else:
				nextChap = None
		if nextChap is None:
			print ("Hoàn Thành Bộ %s" % folderName)
			files.close ()
			break
		else:
			url = nextChap
		delayTimer (10)



story = input ("Nhập link >> ")
if "wattpad" in story:
	getStoryWattpad (story)
elif "wikidth.com" in story:
	getStoryWikidth (story)
elif "wikidth.net" in story:
	getStoryWikidthNet (story)
elif "wikinu.net" in story:
	getStoryWikinuNet (story)
elif "truyenfull" in story:
	getStoryTruyenfull (story)
elif "truyentr" in story:
	getStoryTruyentr (story)
elif "wikisach" in story:
	getStoryWikiSach (story)
else:
	print ('loại web này chưa hỗ trợ')


