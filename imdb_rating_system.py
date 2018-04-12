from bs4 import BeautifulSoup
import sys
try:
	from urllib.request import urlopen
except ImportError:
	from urllib2 import urlopen
import re

class imdb_RS(object):
	def __init__(self, title = '', startYear = '', endYear = '', runtimeminutes = '',\
				 genres = '', company = '', num_result = -1,\
				  controversial = False):
		'''
		The object contains:
		title, year, runtimeminutes, company, num_result, controversial
		search_url
		id_list
		movie_map: key: movie_id, value: rating list
		max_rating
		'''
		year = ''
		if title != '':
			title = 'title?title=' + title.replace(' ', '+')
		if startYear != '' or endYear != '':
			year = '&release_date=' + startYear + ',' + endYear
		if runtimeminutes != '':
			runtimeminutes = '&runtime=' + runtimeminutes
		if company != '':
			company = '&companies=' + company
		if genres != '':
			genres = '&genres=' + genres
		self.name_map = {}
		self.num_result = num_result
		self.controversial = controversial
		self.search_url = 'http://www.imdb.com/search/' + title\
							+ year\
							+ genres\
							+ company\
							+ runtimeminutes
		page_num = 1
		search_url_page = self.search_url + '&page=' + str(page_num) +'&ref_=adv_nxt'
		self.id_list = []
		current_id_list = self.fetch_id_in_one_page(search_url_page)
		while len(current_id_list) != 0:
			self.id_list += current_id_list
			page_num += 1
			search_url_page = self.search_url + '&page=' + str(page_num) +'&ref_=adv_nxt'
			# print(search_url_page)
			current_id_list = self.fetch_id_in_one_page(search_url_page)
			# print(current_id_list)
		self.max_rating = -1
		self.movie_map = {}
		# print(self.id_list)
		for this_id in self.id_list:
			rating_url = 'http://www.imdb.com/title/'+ this_id + '/ratings?ref_=tt_ov_rt'
			# print(rating_url)
			rating_list = self.fetch_rating(rating_url)
			self.movie_map[this_id] = rating_list
			rating_num = sum(rating_list)
			if rating_num > self.max_rating:
				self.max_rating = rating_num

	def rank(self, num_result = -1):
		rank_map = {}
		for key, value in self.movie_map.items():
			rating = float(sum([value[i] * (10 - i) for i in range(10)])) / float(sum(value))
			rank_map[key] = pow(float(rating) / float(10), 2) + pow(float(sum(value)) / float(self.max_rating), 2)
		i = 0
		for key in sorted(rank_map, key = rank_map.__getitem__, reverse = True):
			if i == num_result:
				break
			print('NO.'+str(i+1))
			print(self.name_map[key])
			print('SCORE:', rank_map[key] / 2 * 100)
			i += 1

	def process_data(self, data):
		'''
		helper for review data fetched
		'''
		if data[0] != 'Rating' and data[1] != 'Votes':
			return [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
		i = 3
		result = []
		while i < len(data):
			if data[i] != '0':
				result.append(int(data[i+1].replace(',', '')))
				i += 3
			else:
				result.append(0)
				i += 2
		return result

	def fetch_rating(self, seed):
		'''
		INPUT:	seed(URL)
		OUTPUT:	a list of # of review in order from 10 to 1
		'''
		rating_prec = [3 * i for i in range(1, 10)]
		rating_num = [3 * i + 1 for i in range(1, 10)]
		thisFile = urlopen(seed)
		thishtml = thisFile.read()
		thisFile.close()
		soup = BeautifulSoup(thishtml, 'lxml')
		tables = soup.find_all('table')
		temp = tables[0]
		data = temp.text.replace(u'\xa0', ' ')
		data = data.replace(' ', '').replace('\n', ' ').split()
		# print(data)
		return self.process_data(data)
		# return [int(data[i].replace(',', '')) for i in rating_num]

	def fetch_id_in_one_page(self, seed):
		'''
		INPUT:	seed(URL)
		OUTPUT: a list of id found in one page. If an empty list is returned,
				it means this page has no result.
		'''	
		thisFile = urlopen(seed)
		thishtml = thisFile.read()
		thisFile.close()
		soup = BeautifulSoup(thishtml, 'lxml')
		thisAll = soup.find_all('a')
		id_list = []
		for links in thisAll:
			thisLink = links.get('href')
			if 'title/tt' in thisLink:
				this_id = thisLink[7:16]
				if thisLink[-5:] == 'li_tt':
					# print(thisLink)
					self.name_map[this_id] = links.text
				if thisLink[-5:] == '_li_i':
					# print(thisLink)
					assert this_id not in id_list
					id_list.append(this_id)
		# print(id_list)
		# print(self.name_map)
		return id_list

def main():
	# testurl = 'http://www.imdb.com/title/tt0068646/ratings?ref_=tt_ov_rt'
	# testurl2 = 'http://www.imdb.com/search/title?title=The%20Godfather&page=6&ref_=adv_nxt'
	# rating_num = fetch_rating(testurl)
	# id_list = fetch_id(testurl2)
	# print(id_list)
	temp = imdb_RS('the godfather', '1990-01-01', '1991-01-01')
	temp.rank()

if __name__ == '__main__':
	main()