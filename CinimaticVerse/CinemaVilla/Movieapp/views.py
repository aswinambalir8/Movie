from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import render, redirect,get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import authenticate, login as auth_login
from django.db.models import Q

from .forms import ProfileEditForm,UserProfileForm
from .models import Movie, UserProfile,Category
from .forms import MovieForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def func(request):
    return render(request,'index.html')


def login(request):
    if request.method == 'POST':
        usr = request.POST['username']
        pas = request.POST['password']
        val = authenticate(username=usr, password=pas)

        if val is not None:
            auth_login(request, val)

            # Check if the user has just registered (first login)
            if request.user.is_staff:
                return redirect('admin:index')
            elif val.last_login is None:
                # Redirect to a unique dashboard URL based on user ID
                unique_dashboard_url = f'dashboard/{request.user.id}/'
                return redirect(unique_dashboard_url)
            else:
                return redirect('dashboard')
        else:
            messages.info(request, 'Invalid user')
            return redirect('login')

    return render(request, 'signin.html')


def register(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES)

        if profile_form.is_valid():
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken.')
                return redirect('signup')

            # Check if the email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already taken.')
                return redirect('signup')

            # Validate password
            try:
                validate_password(password1, user=User)
            except ValidationError as e:
                messages.error(request, e)
                return redirect('signup')
            # Check if passwords match
            if password1 != password2:
                messages.error(request, 'Passwords do not match.')
                return redirect('signup')

            # Create a new User
            user = User.objects.create_user(
                username=username,
                password=request.POST['password1'],
                email=email,
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name']
            )

            # Create a new UserProfile
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            messages.success(request, f'Account created for {user.username}', extra_tags='success')
            return redirect('login')

    else:
        profile_form = UserProfileForm()

    return render(request, 'signup.html', {'profile_form': profile_form})
def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    return render(request, 'profile.html', {'user_profile': user_profile, 'created': created})

@login_required
def profile_edit(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        profile_form = ProfileEditForm(request.POST, instance=request.user)
        user_profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if profile_form.is_valid() and user_profile_form.is_valid():
            profile_form.save()
            user_profile_form.save()
            return redirect('profile')  # Redirect to the profile page after editing

    else:
        profile_form = ProfileEditForm(instance=request.user)
        user_profile_form = UserProfileForm(instance=user_profile)

    return render(request, 'profile_edit.html', {'profile_form': profile_form, 'user_profile_form': user_profile_form, 'user_profile': user_profile})

@login_required
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.added_by = request.user
            movie.save()
            return redirect('dashboard')
    else:
        form = MovieForm()

    return render(request, 'add_movie.html', {'form': form})


from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    # Fetch movies specific to the logged-in user
    movie_list = Movie.objects.filter(added_by=request.user)

    # Get the selected category from the query parameters
    selected_category = request.GET.get('category', '')

    # Filter movies based on the selected category
    if selected_category:
        movie_list = movie_list.filter(category__name__icontains=selected_category)

    paginator = Paginator(movie_list, 3)  # Show 3 movies per page

    page = request.GET.get('page')
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        movies = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver the last page.
        movies = paginator.page(paginator.num_pages)

    # Check if there are more than 3 movies to show the paginator
    show_paginator = paginator.count >= 1

    # Get all distinct categories for the category filter
    categories = Category.objects.all()  # Use the correct model name

    return render(request, 'dashboard.html', {'movies': movies, 'show_paginator': show_paginator, 'selected_category': selected_category, 'categories': categories})


@login_required
def movie_details(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    referring_url = request.META.get('HTTP_REFERER')
    search_query = request.GET.get('q', '')
    return render(request, 'movie_details.html', {'movie': movie, 'referring_url': referring_url, 'search_query': search_query})

#to edit our added movie
@login_required
def edit_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id, added_by=request.user)

    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movie_details', movie_id=movie.id)
    else:
        form = MovieForm(instance=movie)

    return render(request, 'edit_movie.html', {'form': form, 'movie': movie})

@login_required
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id, added_by=request.user)
    movie.delete()
    return redirect('dashboard')
# for search movie
@login_required
def search_view(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')  # Get the selected category from the query parameters

    # Perform a case-insensitive search on the title
    results = Movie.objects.filter(Q(title__icontains=query) & Q(added_by=request.user))

    # Filter results by category if a category is selected
    if category:
        results = results.filter(category__name__icontains=category)

    paginator = Paginator(results, 3)  # Show 3 movies per page

    page = request.GET.get('page')
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        search_results = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver the last page.
        search_results = paginator.page(paginator.num_pages)

    # Check if there are more than 3 search results to show the paginator
    show_paginator = paginator.count >= 1

    # Get all distinct categories for the category filter
    categories = Category.objects.all()
    context = {
        'query':query,
        'results': search_results,
        'show_paginator': show_paginator,
        'categories': categories,
        'selected_category': category,
        # Other context data for the search results
    }

    return render(request, 'search_results.html',context)
