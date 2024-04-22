from django import forms
from . import constants
from django.contrib.auth.models import User as djangoUser


class SignInForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    email = forms.CharField(label='email', max_length=100)
    password = forms.CharField(label='password', max_length=100)
    movieGenre = forms.ChoiceField(choices=constants.SignInFormChoices)


class LogInForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    password = forms.CharField(label='password', max_length=100)


class NewMovieForm(forms.Form):
    ShortName = forms.CharField(max_length=25, label="ShortName")
    FullName = forms.CharField(max_length=100, label="FullName")
    Description = forms.CharField(
        max_length=500, label="Description", widget=forms.Textarea())
    Genres = forms.MultipleChoiceField(
        choices=constants.SignInFormChoices, label="Genres")
    MovieLengthMinutes = forms.IntegerField(
        label="MovieLength-Minutes", min_value=0, max_value=59)
    MovieLengthHours = forms.IntegerField(
        label="MovieLength-Hours", min_value=0, max_value=4)
    ReleaseDate = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date'}))  # label="ReleaseDate"


class NewRateForm(forms.Form):
    Rating = forms.IntegerField(
        widget=forms.NumberInput(attrs={"type": "range", "max": 10, "min": 0}))
    Description = forms.CharField(label="", widget=forms.Textarea(
        attrs={"placeholder": "Description (optional)"}), max_length=700, required=False)


class deleteUserForm(forms.Form):
    User = forms.ChoiceField()


class deleteMovieForm(forms.Form):
    Movie = forms.ChoiceField()


class deleteRatingForm(forms.Form):
    Rating = forms.ChoiceField()
