# # IMDb python package
## Introduction:
This is a package which is trying to make fetch information needed from IMDb since there's no official API from IMDb right now. This package can easily fetch all important information one may need about any movie.

## Usage:
Try:
```
from imdb_py import imdb
```

Currently we provide following options:
1. Title (title)
2. Start year (startYear)
3. End year (endYear)
4. Run time (runtime minutes)
5. Genres (genres)
6. Company (company)
7. Number of movies (num_result)

For example, if a user wants to find movies suggestions whose title is related with /The Godfather/ with first 5 titles from IMDb, he can try
```
//produce an imdb object
my_imdb = imdb('the godfather', num_result=5)
```

After you have declared, this object would contain a list of movie title id you need.
```
my_imdb.get_list()
```
It would return a result list of all movie title id you need:
> ['tt0068646', 'tt0071562', 'tt0099674', 'tt0809488', 'tt0388473']

To see the names of the movie, try:
```
my_imdb.get_name()
```
It will return a result map where key is movie title id and value is movie's name:
> {'tt0068646': 'The Godfather'}, {'tt0071562': 'The Godfather: Part II'}, {'tt0099674': 'The Godfather: Part III'}, {'tt0809488': 'The Godfather: A Novel for Television'}, {'tt0388473': 'Tokyo Godfathers'}]

To  see the detail rating of a movie, try:
```
# get a movie title id
this_id = my_imdb.get_list()[0]
# detail_rating has 3 arguments:
# movie_id
# gender = 'males' or 'females', default: ''
# age_group = 'under_18' or '18_29' or '30_44' or '45_plus'
#           default: ''
my_imdb.detail_rating(this_id)
```
It will return a list of movies rating number with first one is number of people who rate 10 and last is the number of people who rate 1
> [696419, 323564, 157803, 62476, 23240, 13392, 6602, 5221, 5072, 34242]

To see detail of a movie, try:
```
# detail has 2 arguements:
# movie_id
# keyword = True or False, default: False
my_imdb.detail(this_id)
```
It will return all important information of a movie:
> {'genre': ['Crime', 'Drama'], 'country': ['USA'], 'company': ['Paramount Pictures', 'Alfran Productions'], 'director': ['Francis Ford Coppola'], 'color': ['Color'], 'rating_num': 1328031}

To see all details of imdb object movie id list, try:
```
# details has 1 arguements:
# keyword = True or False, default: False
my_imdb.details()
```
It will return a map of all important information of movies you searched with key equals to movie title id:
> {'tt0068646': {'genre': ['Crime', 'Drama'], 'country': ['USA'], 'company': ['Paramount Pictures', 'Alfran Productions'], 'director': ['Francis Ford Coppola'], 'color': ['Color'], 'rating_num': 1328031}, 'tt0071562': {'genre': ['Crime', 'Drama'], 'country': ['USA'], 'company': ['Paramount Pictures', 'The Coppola Company'], 'director': ['Francis Ford Coppola'], 'color': ['Color'], 'rating_num': 918226}, 'tt0099674': {'genre': ['Crime', 'Drama'], 'country': ['USA'], 'company': ['Paramount Pictures', 'Zoetrope Studios'], 'director': ['Francis Ford Coppola'], 'color': ['Color'], 'rating_num': 307341}, 'tt0809488': {'genre': ['Crime', 'Drama', 'Thriller'], 'country': ['USA'], 'company': ['American Zoetrope', 'Paramount Pictures'], 'director': [], 'color': ['Color'], 'rating_num': 3443}, 'tt0388473': {'genre': ['Animation', 'Adventure', 'Comedy', 'Drama'], 'country': ['Japan'], 'company': ['Madhouse'], 'director': ['Satoshi Kon', 'Shôgo Furuya'], 'color': ['Color'], 'rating_num': 23650}}

## Other:
You can directly try imdb in tester.py.
If you have any further needs or you find any bugs, please raise an issue. Thank you!