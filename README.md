# IMDB Rating System
## Introduction:
We are trying to make a movie rating system which can fetch information including rating, distribution of rating and reviews to give users a fair suggestion and ranking for movie that they would like to find.

## Usage:
To use this rating system, try:
```
from imdb_rating_system import imdb_RS
temp = imdb_RC()
```

Currently we provide following options:
1. Title (title)
2. Start year (startYear)
3. End year (endYear)
4. Run time (runtime minutes)
5. Genres (genres)
6. Company (company)
7. Number of movies suggested (num_result)

For example, if a user wants to find movie suggestions whose title is related with /The Godfather/, started from Jan. 1, 1990 and ended from Jan. 1, 1991, he can try
```
//produce an imdb_RS object
temp = imdb_RS('the godfather', '1990-01-01', '1991-01-01')
//provide suggestion
temp.rank()
```

The result would show as:
> NO.1
> The Godfather: Part III
> SCORE: 79.49830331785225
> NO.2
> The Godfather Family: A Look Inside
> SCORE: 31.673099302007646
> NO.3
> Godfather of Mimico
> SCORE: 0.5000000005302506
> NO.4
> The Godfather Part III/ Kindergarten Cop / The Bonfire of the Vanities / The Russia House
> SCORE: 0.5000000005302506

## Other:
This is for EECS 486 information retrieval final project, winter 2018.