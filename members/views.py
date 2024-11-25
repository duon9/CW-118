from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.template import loader
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404, Http404
from django.urls import reverse
from .models import Member, Movie, TVSeries, Season, Episode, Genre
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .utils import is_password_strong, check_image_url
import requests
import os
import internetarchive
from django.conf import settings
from urllib.parse import urlparse


# Create your views here.
def members(request):
   mymembers = Member.objects.all().values()
   template = loader.get_template('members.html')
   context = {
      'mymembers': mymembers,
   }
   return HttpResponse(template.render(context, request))

def home(request):
    mymovies = Movie.objects.all().order_by('-id')[:3].values()
    template = loader.get_template("home.html")
    context = {
        'movies' : mymovies
    }
    return HttpResponse(template.render(context, request))

def detail(request, id):

   mymember = Member.objects.get(id=id)
   template = loader.get_template("detail.html")
   context = {
    'mymember': mymember,
    }
   return HttpResponse(template.render(context, request))

def player(request, id):

#    member_id = request.session.get('member_id')
#    if not member_id:
#       # Redirect to sign-in page with 'next' parameter set to the current URL
#       signin_url = reverse('signin')  # Get the URL of the sign-in view
#       return redirect(f'{signin_url}?next={request.path}')
   
   template = loader.get_template("player.html")
   mymovie = get_object_or_404(Movie, id=id)
   suggested_movies = Movie.objects.exclude(id=mymovie.id).order_by('?')[:5]  # Get 5 random suggested movies
   context = {
      "movie" : mymovie,
      "suggested_movies" : suggested_movies
   }
   return HttpResponse(template.render(context, request))

def movies(request):
    # member_id = request.session.get('member_id')
    # if not member_id:
    #     signin_url = reverse('signin')
    #     return redirect(f'{signin_url}?next={request.path}')

    query = request.GET.get('q')
    genre_ids = request.GET.getlist('genres')  # Get a list of selected genre IDs

    # Start with all movies
    movies_list = Movie.objects.all().order_by('-id')

    # Filter by search query if provided
    if query:
        movies_list = movies_list.filter(title__icontains=query)

    # Filter by selected genres if provided
    if genre_ids:
        movies_list = movies_list.filter(genres__id__in=genre_ids).distinct()

    paginator = Paginator(movies_list, 12)  # Show 12 movies per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetch all genres to display in the search form
    genres = Genre.objects.all()

    template = loader.get_template("movies.html")
    context = {
        'page_obj': page_obj,
        'query': query,
        'genres': genres,
        'selected_genres': genre_ids,  # Pass selected genres to template
    }
    return HttpResponse(template.render(context, request))

def tvseries(request):
   query = request.GET.get('q')
   if query:
      series_list = TVSeries.objects.filter(title__icontains=query)
   else:
      series_list = TVSeries.objects.all().order_by('-id')

   paginator = Paginator(series_list, 12)  # Show 12 movies per page
   page_number = request.GET.get('page')
   page_obj = paginator.get_page(page_number)

   template = loader.get_template("tv_series.html")
   context = {
      'page_obj': page_obj,
      'query': query,  # Pass the query to the template
   }
   return HttpResponse(template.render(context, request))

def tvseries_detail(request, id):
   template = loader.get_template("tvseries_detail.html")
   series = get_object_or_404(TVSeries, id = id)
   seasons = series.season_list.all()

   context = {
       "series" : series,
       "seasons" : seasons,
   }

   return HttpResponse(template.render(context, request))
    
def watch(request, id):
    episode = get_object_or_404(Episode, id= id)
    season = episode.season
    series = season.series
    template = loader.get_template("watch.html")
    context = {
        "episode" : episode,
        "series" : series,
        "season" : season
    }
    return HttpResponse(template.render(context, request))

def signin(request):
   next_url = request.GET.get('next')
   if (request.GET.get('next') != None):
         next_url = request.GET.get('next')
         print(next_url)
   else:
         print("home")
         next_url = 'home'

   if request.method == 'POST':
      username = request.POST.get('username')
      password = request.POST.get('password')

      try:
         member = Member.objects.get(username=username)
         if member.check_password(password):
               # Log the user in
               request.session['member_id'] = member.id
               messages.success(request, 'Login successful!')
               return redirect(next_url)
         else:
               messages.error(request, 'Invalid username or password.')
      except Member.DoesNotExist:
         messages.error(request, 'Invalid username or password.')

   return render(request, 'signin.html', {'next': next_url})


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')
        phone = request.POST.get('phone')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')

        # Check if username already exists
        if Member.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('signup')
        if len(username) < 7 or len(username) > 32:
            messages.error(request, 'Username must be in range of 6 to 32 characters')
            return redirect('signup')

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Invalid email address.')
            return redirect('signup')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')
        if (not is_password_strong(password)):
            messages.error(request, "Your password is too weak. Make sure it is at least 8 characters long and includes special characters, uppercase, and lowercase letters.")
            return redirect('signup')
        # Create and save the new member
        member = Member(
            username=username,
            email=email,
            password=make_password(password),
            phone=phone,
            firstname=firstname,
            lastname=lastname
        )
        member.save()
        messages.success(request, 'Registration successful. Please sign in.')
        return redirect('signin')

    return render(request, 'signup.html')

def logout(request):
    request.session.pop('member_id', None)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')

def file_proxy(request):
    file_url = request.GET.get('url')
    if not file_url:
        raise Http404("File URL is required")

    # Validate the URL (basic example; adjust as needed)
    parsed_url = urlparse(file_url)
    if not (parsed_url.scheme and parsed_url.netloc):
        raise Http404("Invalid URL")

    try:
        response = requests.get(file_url, stream=True)
        response.raise_for_status()  # Raises HTTPError for bad responses
    except requests.RequestException as e:
        raise Http404(f"Error fetching file: {str(e)}")

    # Create an HTTP response with the content of the file
    proxy_response = HttpResponse(response.content, content_type=response.headers.get('Content-Type', 'application/octet-stream'))
    proxy_response['Content-Disposition'] = f'attachment; filename="{file_url.split("/")[-1]}"'
    return proxy_response

def profile(request):
   member_id = request.session.get('member_id')
   if not member_id:
      # Redirect to sign-in page with 'next' parameter set to the current URL
      signin_url = reverse('signin')  # Get the URL of the sign-in view
      return redirect(f'{signin_url}?next={request.path}')
   member = get_object_or_404(Member, id = member_id)
   template = loader.get_template("profile.html")
   print(member == None)
   context = {
       "member" : member
   }

   return HttpResponse(template.render(context, request))

def change_avatar(request):
    member_id = request.session.get('member_id')
    if not member_id:
        # Redirect to sign-in page with 'next' parameter set to the current URL
        signin_url = reverse('signin')  # Get the URL of the sign-in view
        return redirect(f'{signin_url}?next={request.path}')

    if request.method == 'POST':
        member = get_object_or_404(Member, id=member_id)
        avatar = request.FILES.get('avatar')

        if avatar:
            # Save the file temporarily
            temp_file_path = os.path.join(settings.MEDIA_ROOT, avatar.name)
            with open(temp_file_path, 'wb+') as temp_file:
                for chunk in avatar.chunks():
                    temp_file.write(chunk)

            # Upload the image to the Internet Archive
            try:
                # Replace 'your-item-id' with the actual item ID or create a new item if needed
                item_id = 'your-item-id'
                item = internetarchive.get_item(item_id)

                # Upload the file
                item.upload(temp_file_path, access_key=settings.INTERNET_ARCHIVE_ACCESS_KEY, secret_key=settings.INTERNET_ARCHIVE_SECRET_KEY)
                #item.wait_for_ingest()

                # Construct the URL to the uploaded file
                file_url = f"https://archive.org/download/{item_id}/{avatar.name}"

                # Check if the uploaded image URL contains valid content
                if check_image_url(file_url):
                    member.avatar = file_url  # Assuming you have an `avatar` field in your Member model
                    member.save()
                else:
                    print("Uploaded image URL does not contain valid content.")
                    # Handle the error accordingly, possibly set a message for the user

                # Remove the temporary file
                os.remove(temp_file_path)

            except Exception as e:
                print(f'Error uploading file: {e}')
                # Handle the error accordingly, possibly set a message for the user

        return redirect('profile')

    return render(request, 'profile.html', {'member': request.user})


def test(request):
    template = loader.get_template("test.html")
    context = {

    }

    return HttpResponse(template.render(context, request))