from django.shortcuts import render
from MovieManager.models import Director, Movie, MovieInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


"""View function for home page of site."""
def index(request):

    # Generate counts of some of the main objects
    num_movies = Movie.objects.all().count()
    num_instances = MovieInstance.objects.all().count()
    num_instances_available = MovieInstance.objects.filter(status__exact='a').count()  
    num_directors = Director.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    
    context = {
        'num_movies': num_movies,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_directors': num_directors,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class MovieListView(generic.ListView):
    model = Movie
    paginate_by = 10


class MovieDetailView(generic.DetailView):
    model = Movie


class DirectorListView(generic.ListView):
    model = Director
    paginate_by = 10


class DirectorDetailView(generic.DetailView):
    model = Director


class RentedMoviesByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = MovieInstance
    template_name ='MovieManager/movieinstance_list_rented_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return MovieInstance.objects.filter(renter=self.request.user).filter(status__exact='o').order_by('due_back')