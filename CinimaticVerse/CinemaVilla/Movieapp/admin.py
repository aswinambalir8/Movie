from django.contrib import admin
from .models import UserProfile,Category, Movie,Quality

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Movie)
admin.site.register(Quality)


