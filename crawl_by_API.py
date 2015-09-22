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
import time
import json
import urllib
import urllib2
from bs4 import BeautifulSoup

class Tuchong_Spider:
	#Init initial url and folder to save photos
	def __init__(self, author, url, num_of_pic):
		self.my_url = url
		self.num_of_pic = int(num_of_pic)
		self.folder = 'photos\\%s' % author
		self.site_id = ''
		self.API = ''
		self.today = time.strftime("%Y-%m-%d")
		print u'Spider initiated.'

	#Get html content of an url
	def get_html(self, url):
		html = urllib2.urlopen(url).read()
		return html

	#spider entrance
	def start(self):
		print u'Start Collecting the most recent %s photos from: %s' %(self.num_of_pic, self.my_url)
		html = self.get_html(self.my_url)
		self.init_site_id(html)
		self.API = self.my_url+"/rest/sites/%s/posts/%s?limit=%s" %(self.site_id,self.today,self.num_of_pic)
		photo_json_str = self.get_html(self.API)

		level1_img_url_list = self.decode_level1_img_url_list_from_json(photo_json_str)
		index = self.download_photos(level1_img_url_list)
		print '%s photos saved in folder: %s.' %(index, self.folder)


	#Download at most num_of_pic of the photos via the level1 urls to level2 urls
	def download_photos(self, level1_img_url_list):
		index = 1
		for level1_img_url in level1_img_url_list:
			print u'Start extracting level 2 url from: ' + level1_img_url
			level2_img_url_list = self.extract_level2_img_url(level1_img_url)	
			for level2_img_url in level2_img_url_list:
				if self.num_of_pic < index:
					return index-1
				self.save_img(level2_img_url, index)
				index+=1
		return index-1
	#Get site_id that specify an author
	def init_site_id(self, html):
		soup = BeautifulSoup(html, 'html.parser')
		post_collages = soup.find("div", attrs={"class":"post-collages"})
		self.site_id = post_collages.get('data-site-id')

	#Get presentation page url for each photo from the initial page
	def decode_level1_img_url_list_from_json(self, photo_json_str):
		parsed_json = json.loads(photo_json_str)
		posts = parsed_json['posts']
		level1_img_url_list = []
		for post in posts:
			level1_img_url_list.append(post['url'])
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

	print u'please enter the number of the photo you want to download at most. eg: 200:'
	num_of_pic = str(raw_input())

	mySpider = Tuchong_Spider(author, url, num_of_pic)
	mySpider.start()