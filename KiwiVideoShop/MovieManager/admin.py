<<<<<<< HEAD
from django.contrib import admin
from MovieManager.models import Director, Movie, MovieInstance, Genre


# Define the admin class
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

# Register the admin class with the associated model
admin.site.register(Director, DirectorAdmin)


class MovieInstanceInline(admin.TabularInline):
    model = MovieInstance


# Register the Admin classes for Movie using the decorator
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'director', 'display_genre', 'year')
    inlines = [MovieInstanceInline]


# Register the Admin classes for MovieInstance using the decorator
@admin.register(MovieInstance) 
class MovieInstanceAdmin(admin.ModelAdmin):
    list_display = ('movie', 'status', 'renter', 'due_back', 'id')
    list_filter = ('status', 'due_back')
    
    fieldsets = (
        (None, {
            'fields': ('movie','imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','renter')
        }),
    )


admin.site.register(Genre)
=======
from django.contrib import admin
from MovieManager.models import Director, Movie, MovieInstance, Genre


# Define the admin class
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

# Register the admin class with the associated model
admin.site.register(Director, DirectorAdmin)


class MovieInstanceInline(admin.TabularInline):
    model = MovieInstance


# Register the Admin classes for Movie using the decorator
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'director', 'display_genre', 'year')
    inlines = [MovieInstanceInline]


# Register the Admin classes for MovieInstance using the decorator
@admin.register(MovieInstance) 
class MovieInstanceAdmin(admin.ModelAdmin):
    list_display = ('movie', 'status', 'renter', 'due_back', 'id')
    list_filter = ('status', 'due_back')
    
    fieldsets = (
        (None, {
            'fields': ('movie','imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','renter')
        }),
    )


admin.site.register(Genre)
>>>>>>> 3af40b1af3ba885ee85a122757be80b887cf83b4
