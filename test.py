from imdb import IMDb

ia = IMDb()
s_result = ia.search_movie('X')
for item in s_result:
   print item['long imdb canonical title'], item.movieID
