from bs4 import BeautifulSoup
import sys
try:
	from urllib.request import urlopen
except ImportError:
	from urllib2 import urlopen
import re

class imdb(object):
	def __init__(self, title = '', startYear = '', endYear = '', runtimeminutes = '',\
				 genres = '', company = '', num_result = -1):
		'''
		The object contains:
		id_list
		search_url
		name_map: key: movie_id, value: name
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
		self.search_url = 'http://www.imdb.com/search/' + title\
							+ year\
							+ genres\
							+ company\
							+ runtimeminutes
		page_num = 1
		search_url_page = self.search_url + '&page=' + str(page_num) +'&ref_=adv_nxt'
		current_id_list, num_result = self.fetch_id_in_one_page(search_url_page, num_result)
		self.id_list = []
		while len(current_id_list) != 0:
			self.id_list += current_id_list
			page_num += 1
			search_url_page = self.search_url + '&page=' + str(page_num) +'&ref_=adv_nxt'
			current_id_list, num_result = self.fetch_id_in_one_page(search_url_page, num_result)

	def get_list(self):
		return self.id_list

	def detail_rating(self, movie_id, gender='', age_group =''):
		assert(gender == 'males' or gender == 'females' or gender == '')
		assert(age_group == 'under_18' or age_group =='18_29' or age_group == '30_44' or age_group =='45_plus' or age_group =='')
		if gender != '':
			gender += '_'
		if age_group != '':
			age_group = 'aged_' + age_group
		seed = 'http://www.imdb.com/title/' + movie_id + '/ratings?demo=' + gender + age_group
		return self.fetch_rating(seed)

	def detail(self, movie_id, keywords=False):
		seed = 'http://www.imdb.com/title/' + movie_id + '/'
		thishtml = urlopen(seed).read()
		soup = BeautifulSoup(thishtml, 'lxml')
		genre_list = []
		kw_list =[]
		country_list = []
		company_list = []
		director_list = []
		color_list = []
		thisAll = soup.find_all('a')
		for links in thisAll:
			thisLink = links.get('href')
			try:
				if 'stry_gnr' in thisLink:
					genre_list.append(links.text[1:])
				if 'country_of_origin' in thisLink:
					country_list.append(links.text)
				if '/company/' in thisLink:
					if 'See More' in links.text:
						continue
					company_list.append(links.text)
				if 'tt_ov_dr' in thisLink:
					if 'more credit' in links.text:
						continue
					director_list.append(links.text)
				if 'colors=' in thisLink:
					color_list.append(links.text)
				if 'tt_ov_rt' in thisLink and 'title' in thisLink:
					rating = int(links.text.replace(',', ''))
			except Exception:
				pass
		detail_map = {}
		
		detail_map['genre'] = genre_list
		detail_map['country'] = country_list
		detail_map['company'] = company_list
		detail_map['director'] = director_list
		detail_map['color'] = color_list
		detail_map['rating_num'] = rating
		if keywords:
			seed = 'https://www.imdb.com/title/' + movie_id + '/keywords?ref_=tt_stry_kw'
			thishtml = urlopen(seed).read()
			soup = BeautifulSoup(thishtml, 'lxml')
			thisAll = soup.find_all('a')
			for links in thisAll:
				thisLink = links.get('href')
				if '/keyword/' in thisLink:
					kw_list.append(links.text)
			detail_map['keyword'] = kw_list
		return detail_map

	def get_name(self):
		rank_list = []
		for movie_id in self.id_list:
			rank_list.append({movie_id: self.name_map[movie_id]})
		return rank_list

	def details(self, keywords=False):
		details_map = {}
		for movie_id in self.id_list:
			details_map[movie_id] = self.detail(movie_id, keywords)	
		return details_map

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
		return self.process_data(data)

	def fetch_id_in_one_page(self, seed, num=-1):
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
			if num == 0:
				break
			thisLink = links.get('href')
			if 'title/tt' in thisLink:
				this_id = thisLink[7:16]
				if thisLink[-5:] == 'li_tt':
					self.name_map[this_id] = links.text
					num -= 1
				if thisLink[-5:] == '_li_i':
					assert this_id not in id_list
					id_list.append(this_id)
		return id_list, num

def main():
	temp = imdb_RS('the godfather', num_result=5)
	print(temp.rank())

if __name__ == '__main__':
	main()