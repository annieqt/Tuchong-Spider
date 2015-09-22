#---------------------------------------
#
#	ATTENTION: NEVER FOR COMMERCIAL USE. 
#	Copyright Reserved by authors.   
#
#	A spider for tuchong pictures: 
#   Collecting pictures of a specified author
#   Author: Tian Wang
#   Date: 2015-09-15
#---------------------------------------
import os
import time
import string
import urllib
import urllib2
from bs4 import BeautifulSoup

class Tuchong_Spider:
	#Init initial url and folder to save photos
	def __init__(self, author, url):
		self.my_url = url
		self.folder = 'photos\\%s' % author
		print u'Spider initiated.'

	#Get html content of an url
	def get_html(self, url):
		html = urllib2.urlopen(url).read()
		return html

	#spider entrance
	def start(self):
		print u'Start Collecting from:' + self.my_url
		html = self.get_html(self.my_url)
		level1_img_url_list = self.find_level1_img_url_list(html)
		index = 0
		for level1_img_url in level1_img_url_list:
			print u'Start extracting level 2 url from: ' + level1_img_url
			level2_img_url_list = self.extract_level2_img_url(level1_img_url)	
			for level2_img_url in level2_img_url_list:
				print level2_img_url
				self.save_img(level2_img_url, index)
				index+=1
		print 'photos saved in ' + self.folder

	#Get presentation page url for each photo from the initial page
	def find_level1_img_url_list(self, html):
		soup = BeautifulSoup(html, 'html.parser')
		level1_img_url_list = []
		print u'Level 1 urls of photos:'			
		for a in soup.find_all("a", attrs={"data-location": "title"}):
			level1_img_url_list.append(a.get('href'))
		return level1_img_url_list

	#Get final image url from the presentation page
	def extract_level2_img_url(self, level1_img_url):
		html = self.get_html(level1_img_url)
		level2_img_url_list = []
		soup = BeautifulSoup(html, 'html.parser')
		for a in soup.find_all("img", attrs={"class":"img-responsive copyright-contextmenu"}):
			level2_img_url_list.append(a.get('src'))
		return level2_img_url_list
		
	#Save image of img_url with index as file name in the folder
	def save_img(self, img_url, index):
		file_name = str(index) +'.jpg'
		if not os.path.exists(self.folder):
			os.makedirs(self.folder)
		target = self.folder +'\\%s' % file_name
		print u'saving picture %s to %s' %(file_name,target)
		img = urllib.urlretrieve(img_url, target)
		time.sleep(1)
		return img

	def scroll_down(self):
		self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
		pass

	def click_more_button(self):
		pass
if __name__ == '__main__':
	print u"""
	#---------------------------------------
	#	ATTENTION: PHOTOS NEVER FOR COMMERCIAL USE. 
	#	Copyright Reserved by authors.   
	#
	#	A spider for tuchong pictures: 
	#	Collecting pictures of a specified author
	#	Author: Tian Wang
	#	Date: 2015-09-15
	#---------------------------------------
	"""

	print u'please enter the prefix of the url of the author''s mainpage. eg: annieqt'
	author = str(raw_input())
	url = 'http://%s.tuchong.com' % author

	mySpider = Tuchong_Spider(author, url)
	mySpider.start()