import datetime
from django.shortcuts import render
from MovieManager.models import Director, Movie, MovieInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from MovieManager.forms import RenewMovieForm
from MovieManager.forms import UpdateMovieForm

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


class MovieInstancesByStaffListView(LoginRequiredMixin,generic.ListView):
    model = MovieInstance
    template_name ='movieinstances_by_staff.html'
    paginate_by = 10
    
    def get_queryset(self):
        return MovieInstance.objects.filter(status='o')


@permission_required('MovieManager.can_mark_returned')
def renew_movie_shop_staff(request, pk):
    """View function for renewing a specific MovieInstance by shop staff member."""
    movie_instance = get_object_or_404(MovieInstance, pk=pk)

    if request.method == 'POST':
        movie_renewal_form = RenewMovieForm(request.POST)

        if movie_renewal_form.is_valid():
            movie_instance.due_back = movie_renewal_form.cleaned_data['renewal_date']
            movie_instance.save()
            return HttpResponseRedirect(reverse('all-rented-movies') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        movie_renewal_form = RenewMovieForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': movie_renewal_form,
        'movie_instance': movie_instance,
    }

    return render(request, 'MovieManager/movie_renew_shop_staff.html', context)


@permission_required('MovieManager.can_mark_returned')
def update_movie_shop_staff(request, pk):
    """View function for renewing a specific MovieInstance by shop staff member."""
    movie_instance = get_object_or_404(MovieInstance, pk=pk)

    if request.method == 'POST':
        movie_update_form = UpdateMovieForm(request.POST)

        if movie_update_form.is_valid():
            movie_instance.status = movie_update_form.data['status']
            movie_instance.save()
            return HttpResponseRedirect(reverse('all-rented-movies') )

    # If this is a GET (or any other method) create the default form.
    else:
        movie_update_form = UpdateMovieForm(initial={'status': "m"})

    context = {
        'form': movie_update_form,
        'movie_instance': movie_instance,
    }

    return render(request, 'MovieManager/movie_update_shop_staff.html', context)