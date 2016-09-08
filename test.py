from imdb import IMDb


ia = IMDb()

s_result = ia.search_movie('The Untouchables')

# Print the long imdb canonical title and movieID of the results.
for item in s_result:
   print item['long imdb canonical title'], item.movieID