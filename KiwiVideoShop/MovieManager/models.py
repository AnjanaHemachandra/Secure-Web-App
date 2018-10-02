from django.db import models
from django.urls import reverse
import uuid # Required for unique movie instances
from django.contrib.auth.models import User
from datetime import date


class Movie(models.Model):
    """Model representing a movie (but not a specific copy of a movie)."""
    title = models.CharField(max_length=200)
    director = models.ForeignKey('Director', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the movie.')
    genre = models.ManyToManyField('Genre', help_text='Select a genre for this movie.')
    year = models.CharField(max_length=4)
    
    def __str__(self):
        """String for representing the Model object."""
        return self.title
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this movie."""
        return reverse('movie-detail', args=[str(self.id)])

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    
    display_genre.short_description = 'Genre'


class Director(models.Model):
    """Model representing an director."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']
    
    def get_absolute_url(self):
        """Returns the url to access a particular director instance."""
        return reverse('director-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'


class MovieInstance(models.Model):
    """Model representing a specific copy of a movie (i.e. that can be rented from the shop)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular movie across whole shop.')
    movie = models.ForeignKey('Movie', on_delete=models.SET_NULL, null=True) 
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    renter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Movie availability',
    )

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set Movie As Returned"),)  

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.movie.title}) ({self.imprint})'

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
            return False


class Genre(models.Model):
    """Model representing a Movie genre."""
    name = models.CharField(max_length=200, help_text='Enter a Movie genre (e.g. Science Fiction)')
    
    def __str__(self):
        """String for representing the Model object."""
        return self.name

