from imdb_py import imdb

temp = imdb('the godfather', num_result=5)
print(temp.rank())