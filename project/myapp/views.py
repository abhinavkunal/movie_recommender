from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
from json import dumps

ratings_df = pd.read_csv('ratings.csv')
movies_df = pd.read_csv('movies.csv')
merged_data = pd.merge(ratings_df, movies_df)
merged_data = merged_data.drop(['timestamp', 'genres'], axis=1)
# pivot_data = merged_data.pivot_table(index=['userId'], columns=['title'], values='rating', fill_value=2.5)
pivot_data = merged_data.pivot_table(index=['userId'], columns=['title'], values='rating')
pivot_data = pivot_data.dropna(thresh=5, axis=1).fillna(2.5)
final_matrix = pivot_data.corr(method="pearson")    # final co-relation matrix

names = pivot_data.columns          # a series that contains name of all the movies
combined_df = pd.DataFrame()        # DataFrame used for multiple inputs
movie_rated = []                    # contains names of movies that has been rated so they are not printed in the output

dictionary = {}                     # dictionary to pass to javascript for dropdown suggestions
temp = []                           # list to contain all the movie names for the dictionary for search suggestion
for x in names:
    temp.append(x)
dictionary['list'] = temp

def index(request):     # Initial function to be executed

    dataJSON = dumps(dictionary)
    return render(request, "index.html", {'data': dataJSON})

def reset(request):     # when resetting the values

    global temp
    global movie_rated
    global combined_df
    combined_df = pd.DataFrame()
    for x in movie_rated:
        temp.append(x)
    temp.sort()
    movie_rated.clear()                 # clear the list contains names of previously rated movies
    dataJSON = dumps(dictionary)
    return render(request, "index.html", {'data': dataJSON})

def sub(request):       # called after clicking submit button

    if request.method == "POST":
        name = request.POST['name']
        rating = int(request.POST['rating'])

    global combined_df
    global movie_rated

    if name in names:
        movie_rated.append(name)                    # add the rated movie name to the rated list
        movie_rating_list = final_matrix[name] * (rating - 2.5)     # series containing values of co-efficient of correlation for all the movie
        combined_df = combined_df.append(movie_rating_list)
        temp.remove(name)                           # remove the movie from search suggestion whose rating is given

    final_movie_list = combined_df.sum()        # add all the values in dataframe column wise
    final_movie_list = final_movie_list.sort_values(ascending=False)        # sort all the values
    final_list = []                             # contains the name of recommended movies

    for movie_name, score in final_movie_list.iteritems():
        if movie_name not in movie_rated:       # adding those movie to the list whose rating has not been given
            final_list.append(movie_name)

    dataJSON = dumps(dictionary)
    return render(request, "index.html", {'data': dataJSON, 'value1': final_list})