from django.contrib import admin
from .models import Member, Movie, TVSeries, Season, Episode, Actor, Genre

# Register your models here.

class MemberAdmin(admin.ModelAdmin):
    list_display = ("username", "firstname", "lastname", "phone", "email")
    search_fields = ("username",)

class Movies(admin.ModelAdmin):
    list_display = ("title", "description", "source", "image_src")
    search_fields = ("title",)

class TVseries(admin.ModelAdmin):
    list_display = ("title", "description", "release_date", "genre", "seasons", "episodes", "created_at", "updated_at", "thumbnail",)

class Seasons(admin.ModelAdmin):
    list_display = ("series", "number", "title", "description", "release_date", "thumbnail", "episodes",)

class Episodes(admin.ModelAdmin):
    list_display = ("season", "number", "title", "description", "release_date", "duration", "source")

class Genres(admin.ModelAdmin):
    list_display = ("name",)

class Actors(admin.ModelAdmin):
    list_display = ("name", "dob", "image")

admin.site.register(Member, MemberAdmin)
admin.site.register(Movie, Movies)
admin.site.register(TVSeries, TVseries)
admin.site.register(Season, Seasons)
admin.site.register(Episode, Episodes)
admin.site.register(Actor, Actors)
admin.site.register(Genre, Genres)
