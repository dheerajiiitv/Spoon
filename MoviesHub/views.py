from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
import requests
from threading import Thread
from Spoon.settings import TMDB_KEY
import queue
import time

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
    if movie_id:
        primary_info_link = 'https://api.themoviedb.org/3/movie/'+str(movie_id)+'?api_key='+TMDB_KEY
        alternative_link = 'https://api.themoviedb.org/3/movie/'+str(movie_id)+'/alternative_titles?api_key='+TMDB_KEY
        cast_link = 'https://api.themoviedb.org/3/movie/'+str(movie_id)+'/credits?api_key='+TMDB_KEY
        images_link = 'https://api.themoviedb.org/3/movie/'+str(movie_id)+'/images?api_key='+TMDB_KEY
        plot_keywords_link = 'https://api.themoviedb.org/3/movie/'+str(movie_id)+'/keywords?api_key='+TMDB_KEY
        release_info_link = 'https://api.themoviedb.org/3/movie/'+str(movie_id)+'/release_dates?api_key='+TMDB_KEY
        videos_link = 'https://api.themoviedb.org/3/movie/'+str(movie_id)+'/videos?api_key='+TMDB_KEY
        reviews_link = 'https://api.themoviedb.org/3/movie/'+str(movie_id)+'/reviews?api_key='+TMDB_KEY
        # Taking too much time (calling multiple API) Using threads
        # Queue is used to store all data
        data = queue.Queue()
        primary_info_data = GetData(primary_info_link,data,'primary_info_data')
        alternative_data = GetData(alternative_link,data,'alternative_data')
        cast_data = GetData(cast_link,data,'cast_data')
        images_data = GetData(images_link,data,'images_data')
        plot_keywords_data = GetData(plot_keywords_link,data,'plot_keywords_data')
        release_info_data = GetData(release_info_link,data,'release_info_data')
        videos_data = GetData(videos_link,data,'videos_data')
        reviews_data = GetData(reviews_link,data,'reviews_data')
        primary_info_data.start()
        alternative_data.start()
        cast_data.start()
        images_data.start()
        plot_keywords_data.start()
        release_info_data.start()
        videos_data.start()
        reviews_data.start()
        real_data = {}
        for d in range(8):
            temp = data.get()
            real_data[temp[0]] = temp[1]
        # Data Format
        return render(request, 'MoviesHub/movie_details.html', {'real_data':real_data})
    else:
        redirect('MoviesHub:index')

class GetData(Thread):
    def __init__(self, link,q, field):
        super(GetData, self).__init__()
        self.link = link
        self.q = q
        self.field = field

    def run(self):
        response = requests.get(self.link)
        if response.status_code == 200:
            temp = []
            temp.append(self.field)
            temp.append(response.json())
            self.q.put(temp)
        else:
            print('Error!', self.link)
            return {}