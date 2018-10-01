from django.urls import path
from MovieManager import views


urlpatterns = [
	path('', views.index, name='index'),
	path('movies/', views.MovieListView.as_view(), name='movies'),
	path('movie/<int:pk>', views.MovieDetailView.as_view(), name='movie-detail'),
	path('directors/', views.DirectorListView.as_view(), name='directors'),
	path('director/<int:pk>', views.DirectorDetailView.as_view(), name='director-detail'),
]

urlpatterns += [   
    path('mymovies/', views.RentedMoviesByUserListView.as_view(), name='my-rented'),
]