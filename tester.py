from imdb_py import imdb
my_imdb = imdb('the godfather', num_result=5)

print(my_imdb.get_list())
print(my_imdb.get_name())
this_id = my_imdb.get_list()[0]
print(my_imdb.detail_rating(this_id))
print(my_imdb.detail(this_id))
print(my_imdb.detail(this_id, keywords = True))
print(my_imdb.details())