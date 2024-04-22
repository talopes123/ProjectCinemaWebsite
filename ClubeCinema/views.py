from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth.models import User
from . import forms, constants, models
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as LoginAuth
from django.contrib.auth.decorators import login_required, user_passes_test
import json


def permsLevel_check(user):
    if user.is_authenticated:
        try:
            return user.is_superuser or (models.Profile.objects.get(User_id=user.id).UserLevel == 1)
        except Exception as e:
            print(f"EXCEPTION AT permsLevel_check func -> {e}")
            return False
    else:
        return False


def index(request):
    #try:
       #Profile = models.Profile.objects.get(pk=id)

       return render(request, "movies.html", {
           "loggedIn": request.user.is_authenticated,
           "User": request.user,
           "isAdmin": permsLevel_check(request.user),
           "Movies": models.Movie.objects.all(),
       #    "Profiles": Profile,
       #    "Ratings": models.Rating.objects.filter(Profile_id=Profile.id),
           "Profiles": models.Profile.objects.all(),


    })
    #except Exception as e:
     #  print(f"EXCEPTION AT profile view func -> {e}")
      # return redirect("/")


def ratings(request):
    return render(request, "ratings.html", {
        "loggedIn": request.user.is_authenticated,
        "User": request.user,
        "isAdmin": permsLevel_check(request.user),
        "Ratings": models.Rating.objects.all()
    })


def profiles(request):
    return render(request, "profiles.html", {
        "loggedIn": request.user.is_authenticated,
        "User": request.user,
        "isAdmin": permsLevel_check(request.user),
        "Profiles": models.Profile.objects.all()
    })


def profile(request, id):
    #try:
        Profile = models.Profile.objects.get(pk=id)
        return render(request, "profile.html", {
            "loggedIn": request.user.is_authenticated,
            "User": request.user,
            "isAdmin": permsLevel_check(request.user),
            "Profile": Profile,
            "Ratings": models.Rating.objects.filter(Profile_id=Profile.id),
        })
    #except Exception as e:
     #  print(f"EXCEPTION AT profile view func -> {e}")
      # return redirect("/")


@login_required
@user_passes_test(permsLevel_check)
def admin(request):
    return render(request, "admin.html", {
        "Users": User.objects.all(),
        "Profiles": models.Profile.objects.all(),
        "Movies": models.Movie.objects.all(),
        "Ratings": models.Rating.objects.all(),
        "loggedIn": request.user.is_authenticated,
        "User": request.user,
        "isAdmin": permsLevel_check(request.user)
    })


def login(request):
    if request.method == "POST":
        form = forms.LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            try:
                auth = authenticate(
                    request, username=username, password=password)
                if auth is not None:
                    LoginAuth(request, auth)
            except Exception as e:
                print(f"EXCEPTION AT login view func POST -> {e}")
        return redirect("/")
    elif (request.method == "GET"):
        return render(request, "login.html", {
            "loggedIn": request.user.is_authenticated,
            "MovieGenres": constants.MovieGenres,
            "User": request.user,
            "isAdmin": permsLevel_check(request.user)
        })


def logOut(request):
    logout(request)
    return redirect("/")


@login_required
@user_passes_test(permsLevel_check)
def deleteUser(request):
    if request.method == "POST":
        form = forms.deleteUserForm(request.POST)
        try:
            user = User.objects.get(id=int(form.data["User"])).delete()
            return redirect("/")
        except KeyError:
            pass
    return render(request, "deleteUser.html", {
        "loggedIn": request.user.is_authenticated,
        "User": request.user,
        "isAdmin": permsLevel_check(request.user),
        "Users": User.objects.all()
    })


@login_required
@user_passes_test(permsLevel_check)
def deleteMovie(request):
    if request.method == "POST":
        form = forms.deleteMovieForm(request.POST)
        try:
            movie = models.Movie.objects.get(
                id=int(form.data["Movie"])).delete()
            return redirect("/")
        except KeyError:
            pass
    return render(request, "deleteMovie.html", {
        "loggedIn": request.user.is_authenticated,
        "User": request.user,
        "isAdmin": permsLevel_check(request.user),
        "Movies": models.Movie.objects.all()
    })


@login_required
@user_passes_test(permsLevel_check)
def deleteRating(request):
    if request.method == "POST":
        form = forms.deleteRatingForm(request.POST)
        try:
            rating = models.Rating.objects.get(
                id=int(form.data["Rate"])).delete()
            return redirect("/")
        except Exception as e:
            print(f"EXCEPTION AT deleteRating view func -> {e}")
    return render(request, "deleteRating.html", {
        "loggedIn": request.user.is_authenticated,
        "User": request.user,
        "isAdmin": permsLevel_check(request.user),
        "Ratings": models.Rating.objects.all(),
    })


def movieRate(request, id):
    if request.method == "POST":
        form = forms.NewRateForm(request.POST)
        if (form.is_valid()):
            try:
                movie = models.Movie.objects.get(id=id)
                user = User.objects.get(id=request.user.id)
                Profile = models.Profile.objects.get(User=user)
                Description = (form.cleaned_data["Description"], None)[
                    not form.cleaned_data["Description"]]
                Rating = form.cleaned_data["Rating"]
                try:
                    rate = models.Rating(Movie=movie, Profile=Profile,
                                         Rating=Rating, Description=Description)
                    print(rate)
                    print(rate.Description)
                except Exception as e:
                    print(e)
                rate.save()
                return redirect("/")
            except Exception as e:
                print(f"EXCEPTION AT movieRate view func POST -> {e}")

                return HttpResponseNotFound()
    elif request.method == "GET":
        try:
            return render(request, "movieRate.html", {
                "loggedIn": request.user.is_authenticated,
                "User": request.user,
                "isAdmin": permsLevel_check(request.user),
                "Movie": models.Movie.objects.get(id=id),
                "form": forms.NewRateForm
            })
        except Exception as e:
            print(f"EXCEPTION AT movieRate view func GET -> {e}")


@login_required
@user_passes_test(permsLevel_check)
def newMovie(request):
    if request.method == "POST":
        form = forms.NewMovieForm(request.POST)
        if form.is_valid():
            movie = models.Movie(
                ShortName=form.cleaned_data["ShortName"],
                FullName=form.cleaned_data["FullName"],
                Description=form.cleaned_data["Description"],
                Genres=json.dumps(form.cleaned_data["Genres"]),
                MovieLength=form.cleaned_data["MovieLengthMinutes"] *
                60 + form.cleaned_data["MovieLengthHours"]*3600,
                ReleaseDate=form.cleaned_data["ReleaseDate"]
            )
            movie.save()
            return redirect("/")
        else:
            print("not valid")
    elif request.method == "GET":
        theform = forms.NewMovieForm()
        return render(request, "newMovie.html", {
            "loggedIn": request.user.is_authenticated,
            "User": request.user,
            "isAdmin": permsLevel_check(request.user),
            "form": theform
        })


def signin(request):
    if request.method == "POST":
        form = forms.SignInForm(request.POST)
        if (form.is_valid()):
            email = form.cleaned_data["email"]
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            movieGenre = form.cleaned_data["movieGenre"]

            userAuthModel = User.objects.create_user(
                username=username, password=password, email=email)
            userAuthModel.save()
            profile = models.Profile(
                User=userAuthModel, FavMovieGenre=movieGenre)
            profile.save()
            UserAuth = authenticate(
                request, username=username, password=password)
            if UserAuth is not None:
                LoginAuth(request, UserAuth)
                return render(request, "index.html", {
                    "loggedIn": request.user.is_authenticated,
                    "User": request.user,
                    "isAdmin": permsLevel_check(request.user)
                })
            else:
                return render(request, "login.html", {
                    "error": True,
                    "loggedIn": request.user.is_authenticated,
                    "User": request.user,
                    "isAdmin": permsLevel_check(request.user)
                })
    return render(request, "login.html", {"signin": True, "MovieGenres": constants.MovieGenres})


def movies(request):
    return render(request, "movies.html", {
        "loggedIn": request.user.is_authenticated,
        "User": request.user,
        "isAdmin": permsLevel_check(request.user),
        "Movies": models.Movie.objects.all()
    })
