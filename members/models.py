from django.db import models
import ffmpeg
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
class Member(models.Model):
    id = models.IntegerField(primary_key=True)
    avatar = models.URLField(blank=True)
    username = models.CharField(max_length=255, unique=True, null=False)
    password = models.CharField(max_length=255, null=False)
    firstname = models.CharField(max_length=255, null=True)
    lastname = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=255, null=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"
    

class Genre(models.Model):
    name = models.CharField(max_length=255, blank=False, unique=True)
    movies = models.ManyToManyField('Movie', related_name="genre_list", blank=True)

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=255, blank=False, unique=True)
    dob = models.DateField(blank=True)
    image = models.URLField(blank=True)
    films = models.ManyToManyField('Movie', related_name="actor_list", blank=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255, null=False, unique=True)
    description = models.TextField(null=True, unique=False)
    source = models.CharField(max_length=255, null=True)
    source1 = models.CharField(blank=True, max_length=255)
    image_src = models.CharField(max_length=255, null=True)
    subtitle = models.TextField(blank=True)
    genres = models.ManyToManyField(Genre, related_name="movie_list", blank=True)

    def __str__(self):
        return self.title


class TVSeries(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    release_date = models.DateField(null=True, blank=True)
    genre = models.CharField(max_length=100, blank=True)
    seasons = models.PositiveIntegerField(default=1)
    episodes = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    thumbnail = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Season(models.Model):
    series = models.ForeignKey(TVSeries, on_delete=models.CASCADE, related_name='season_list')
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    release_date = models.DateField(null=True, blank=True)
    thumbnail = models.TextField(blank=True)
    episodes = models.PositiveIntegerField(default=1)
    trailer_url = models.TextField(blank=True)

    def __str__(self):
        return f"{self.series.title} - Season {self.number}"


class Episode(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='episode_list')
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    release_date = models.DateField(null=True, blank=True)
    duration = models.PositiveIntegerField(help_text="Duration in minutes", null=True, blank=True)
    source = models.TextField(blank=True)
    subtitle = models.TextField(blank=True)

    def __str__(self):
        return f"{self.season.series.title} - Season {self.season.number}, Episode {self.number}"


class Bookmark(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="bookmarks")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="bookmarked_by", null=True, blank=True)
    tv_series = models.ForeignKey(TVSeries, on_delete=models.CASCADE, related_name="bookmarked_by", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('member', 'movie', 'tv_series')  # Ensure one bookmark per member per movie/TV series

    def __str__(self):
        return f"Bookmark of {self.member} on {self.movie or self.tv_series}"


class Like(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="likes")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="liked_by", null=True, blank=True)
    tv_series = models.ForeignKey(TVSeries, on_delete=models.CASCADE, related_name="liked_by", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('member', 'movie', 'tv_series')  # Ensure one like per member per movie/TV series

    def __str__(self):
        return f"Like by {self.member} on {self.movie or self.tv_series}"


class View(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="views")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="viewed_by", null=True, blank=True)
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name="viewed_by", null=True, blank=True)
    view_time = models.DateTimeField(auto_now_add=True)
    duration = models.PositiveIntegerField(help_text="Duration in minutes", null=True, blank=True)

    class Meta:
        unique_together = ('member', 'movie', 'episode')  # Ensure one view per member per movie/episode

    def __str__(self):
        return f"View by {self.member} on {self.movie or self.episode}"


class Comment(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="comments")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="comments", null=True, blank=True)
    tv_series = models.ForeignKey(TVSeries, on_delete=models.CASCADE, related_name="comments", null=True, blank=True)
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name="comments", null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.member} on {self.movie or self.tv_series or self.episode}"




