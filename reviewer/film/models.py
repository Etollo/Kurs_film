from django.db import models


class Actor(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    second_name = models.CharField(max_length=200, null=True)
    birthday = models.DateField()
    movies = models.CharField(max_length=300, null=True, blank=True)
    category = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='photos/actors', null=True, blank=True)

    def __str__(self):
        return self.last_name


class Director(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    second_name = models.CharField(max_length=200, null=True)
    birthday = models.DateField()
    movies = models.CharField(max_length=300, null=True, blank=True)
    category = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='photos/directors', null=True, blank=True)

    def __str__(self):
        return self.last_name


class Review(models.Model):
    review = models.TextField(max_length=200)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.review


class News(models.Model):
    head = models.CharField(max_length=100, null=False, blank=False)
    text_news = models.TextField(max_length=500, null=False, blank=False)
    image = models.ImageField(upload_to='news')

    def __str__(self):
        return self.head


class Film(models.Model):
    name_film = models.CharField(max_length=300, unique_for_date=True)
    date_premiere = models.DateField()
    genre = models.CharField(max_length=100, unique=True)
    time = models.IntegerField(null=True, blank=True)
    actor = models.CharField(Actor, max_length=200)
    rating_age = models.IntegerField()
    poster = models.ImageField(upload_to='posters', null=True, blank=True)
    review = models.CharField(Review, max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    actor_dubbing = models.CharField(Actor, max_length=200)
    comment = models.TextField(max_length=200)
    director = models.CharField(Director, max_length=200)
    news = models.CharField(News, max_length=100)

    def __str__(self):
        return self.name_film
