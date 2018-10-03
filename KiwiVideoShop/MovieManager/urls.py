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

urlpatterns += [   
    path('allrentedmovies/', views.MovieInstancesByStaffListView.as_view(), name='all-rented-movies'),
]

urlpatterns += [   
    path('movie/<uuid:pk>/renew/', views.renew_movie_shop_staff, name='renew-movie-shop-staff'),
]

urlpatterns += [   
    path('movie/<uuid:pk>/update/', views.update_movie_shop_staff, name='update-movie-shop-staff'),
]