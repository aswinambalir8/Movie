from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default_image.png')
    date_of_birth = models.DateField(blank=True, null=True)
    # Additional fields
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.user.username

#for catagory
class Category(models.Model):
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name
#for quality
class Quality(models.Model):
    name = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return self.name


#for uploading movie
class Movie(models.Model):
    title = models.CharField(max_length=255)
    poster = models.ImageField(upload_to='movie_posters/')
    description = models.TextField()
    movie_rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    quality = models.ForeignKey(Quality, on_delete=models.SET_NULL, null=True, blank=True)
    release_date = models.DateField()
    actors = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    trailer_link = models.URLField(help_text="Provide the YouTube video URL (e.g., https://youtu.be/abcd1234)")
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title