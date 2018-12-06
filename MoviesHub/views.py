from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
import requests

from Spoon.settings import TMDB_KEY


# Create your views here.
def index(request):
    # Function to show home page.

    if request.method == 'POST':
        # If user submitted a query
        query = request.POST.get('query')
        page = request.POST.get('page', 1)
        if query:
            link = "https://api.themoviedb.org/3/search/movie?api_key=" + TMDB_KEY + "&include_adult=true&query=" \
                   + query + "&page=" + str(page)
            response = requests.get(link)
            if response.status_code == 200:
                json_data = response.json()
                results = json_data['results']
                page_no = json_data['page']
                total_pages = json_data['total_pages']
                return render(request, 'MoviesHub/movies_list.html',
                              {'movies': results, 'query': query, 'page_no': page_no, 'total_pages': total_pages})

            else:
                messages.error(request, "TMDB API not working")
                return redirect('MoviesHub:index')

            return render(request, 'MoviesHub/index.html')
        else:
            try:
                messages.error(request, "No query provided")
            except:
                print("error")
            return redirect('MoviesHub:index')
        # Call API

    else:
        return render(request, 'MoviesHub/index.html')


def get_movie_details(request, movie_id):
    pass
