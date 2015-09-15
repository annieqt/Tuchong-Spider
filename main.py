# -*- coding: utf-8 -*-
#---------------------------------------
#   A spider for tuchong pictures: 
#   Collecting pictures of a specified author
#   Author: Tian Wang
#   Date: 2015-09-15
#---------------------------------------

import string
import urllib
import urllib2
from bs4 import BeautifulSoup

class Tuchong_Spider:
	def __init__(self, url):
		self.my_url = url
		self.folder = ''
		print u'Spider initiated.'

	def get_html(self, url):
		html = urllib2.urlopen(url).read()
		return html

	def start(self):
		print u'Start Collecting from:' + self.my_url
		f = open('test.html', 'w+')
		html = self.get_html(self.my_url)
		f.write(html)
		f.close()
		img_url_list_level1 = self.get_img_url_list_level1(html)
		for img_url_level1 in img_url_list_level1:
			print img_url_level1
			pass

	def get_img_url_list_level1(self, html):
		soup = BeautifulSoup(html, 'html.parser')
		img_url_list_level1 = soup.find(id="post-collage")
		return img_url_list_level1
		

	def save_img(img_url, file_name):
		file_path = 'pics'
		if not os.path.exists(file_path):
			os.makedirs(file_path)
		target = file_path +'\\%s' % file_name
		print u'saving picture %s to %s' %(file_name,file_path)
		img = urllib.urlretrieve(img_url, target)
		time.sleep(1)
		return img









if __name__ == '__main__':
	print u"""
	#---------------------------------------
	#   A spider for tuchong pictures: 
	#   Collecting pictures of a specified author
	#   Author: Tian Wang
	#   Date: 2015-09-15
	#---------------------------------------
	"""

	print u'please enter the prefix of the url of the author''s mainpage:'
	url = 'http://'+str(raw_input())+'.tuchong.com'

	mySpider = Tuchong_Spider(url)
	mySpider.start()